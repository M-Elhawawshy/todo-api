from django.urls import path, include

from auth_service.views import Signup, CookieLoginView, CookieRefresh, Logout
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

urlpatterns = [
    path('signup/', Signup.as_view()),
    path('login/', CookieLoginView.as_view()),

    path('refresh/', CookieRefresh.as_view()),

    path('logout/', Logout.as_view()),
]
