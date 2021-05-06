from two_factor.views import (
    BackupTokensView, ProfileView, QRGeneratorView, SetupCompleteView,
)

from django.contrib.auth import views as auth_views
from django.urls import path

from accounts.forms import CustomOTPAuthenticationForm
from accounts.views import logout_modal, otp_remove, SetupView, otp_setup


urlpatterns = [
    path("login/", auth_views.LoginView.as_view(authentication_form=CustomOTPAuthenticationForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("logout-modal/", logout_modal, name="logout_modal"),
    path(
        'two-factor/profile/',
        ProfileView.as_view(),
        name='profile',
    ),
    path(
        'two-factor/qrcode/',
        QRGeneratorView.as_view(),
        name='qr',
    ),
    path(
        'two-factor/setup/complete/',
        SetupCompleteView.as_view(),
        name='setup_complete',
    ),
    path(
        'two-factor/backup/tokens/',
        BackupTokensView.as_view(),
        name='backup_tokens',
    ),
    path(
        'two-factor/remove/',
        otp_remove,
        name='otp_remove',
    ),
    path(
        'two-factor/setup/',
        otp_setup,
        name='setup',
    ),
    path('test/', otp_setup, name="test")
]
