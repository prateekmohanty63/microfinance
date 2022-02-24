from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('verify', VerifyUserLinkView.as_view(), name='verify'),
    path('forgot-password', VerifyUserLinkView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('create-new-password', CreateNewPasswordView.as_view(), name='create_new_password'),
]
