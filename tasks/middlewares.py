from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken


def get_token_from_header(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    return auth_header.split(' ')[1]


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/tasks'):
            token = get_token_from_header(request)
            if token is None:
                return JsonResponse({"detail": "Missing access token"}, status=401)

            try:
                access_token = AccessToken(token)
                user_id = access_token.get("user_id")
                request.user_id = user_id
            except Exception:
                return JsonResponse({"detail": "Invalid or expired token"}, status=401)

        return self.get_response(request)