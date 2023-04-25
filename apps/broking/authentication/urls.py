from django.contrib.auth.views import LogoutView
from django.urls import path, include

from apps.broking.authentication.views import (
    LoginView, SignupView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', SignupView.as_view(), name="register"),
    path('forgotten-password/', SignupView.as_view(), name="register"),
]
