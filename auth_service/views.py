from http import HTTPStatus

import rest_framework.status
import rest_framework_simplejwt.tokens
from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, token_refresh

from auth_service.serializers import SignupSerializer, RefreshSerializer, LogoutSerializer
from tasks.models import TasksUser


# Create your views here.
class Signup(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CookieLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        refresh_token = response.data.get("refresh")
        access_token = response.data.get("access")

        # Remove refresh token from body (optional for security)
        response.data.pop("refresh", None)

        # Set refresh token in HttpOnly cookie
        response.set_cookie(
            key="refresh",
            value=refresh_token,
            httponly=True,
            secure=False,  # only over HTTPS in production
            samesite="Lax",  # or "Strict"
            path="/api/auth_service/refresh/",
        )

        return response


class CookieRefresh(CreateAPIView):
    serializer_class = RefreshSerializer
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if not refresh_token:
            return Response("no refresh token provided", status=status.HTTP_400_BAD_REQUEST)


        try:
            refresh = rest_framework_simplejwt.tokens.RefreshToken(refresh_token)
            refresh.check_blacklist()
        except TokenError:
            return Response("token blacklisted or invalid", status=status.HTTP_400_BAD_REQUEST)

        user_id = refresh.get("user_id")
        refresh.blacklist()

        try:
            user = TasksUser.objects.get(id=user_id)
        except TasksUser.DoesNotExist:
            return Response("user_id claim invalid", status=status.HTTP_400_BAD_REQUEST)


        refresh = RefreshToken.for_user(user)

        data = {
            'access': str(refresh.access_token)
        }
        response = Response(data, status=status.HTTP_200_OK)
        response.set_cookie(
            key='refresh',
            value=str(refresh),
            httponly=True,
            samesite='Lax',
            path='/api/auth_service/refresh/',
        )
        return response


class Logout(CreateAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if not refresh_token:
            return Response("no refresh token provided", status=status.HTTP_400_BAD_REQUEST)

        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie("refresh")
        return response