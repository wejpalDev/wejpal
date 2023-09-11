from django.urls import path
from .views import *

urlpatterns = [
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password/<str:uidb64>/<str:token>/', PasswordResetView.as_view(), name='password-reset'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('login/', UserLoginView.as_view(), name='login')
]