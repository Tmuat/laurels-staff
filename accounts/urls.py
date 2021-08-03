from two_factor.views import (
    ProfileView,
    SetupCompleteView,
)

from django.contrib.auth import views as auth_views
from django.urls import path

from accounts.forms import CustomOTPAuthenticationForm
from accounts.views import (
    logout_modal,
    otp_remove,
    otp_setup,
    otp_backup,
    QRGeneratorView,
    CustomPasswordResetConfirmView
)


app_name = "accounts"
urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            authentication_form=CustomOTPAuthenticationForm
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("logout-modal/", logout_modal, name="logout_modal"),
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            success_url="done/"
        ),
        name="password-change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password-change-done",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            success_url="done/"
        ),
        name="password-reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password-reset-done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password-reset-complete",
    ),
    path(
        "two-factor/profile/",
        ProfileView.as_view(),
        name="tfa-profile",
    ),
    path(
        "two-factor/qrcode/",
        QRGeneratorView.as_view(),
        name="qr",
    ),
    path(
        "two-factor/setup/complete/",
        SetupCompleteView.as_view(),
        name="setup_complete",
    ),
    path(
        "two-factor/remove/",
        otp_remove,
        name="otp_remove",
    ),
    path(
        "two-factor/setup/",
        otp_setup,
        name="otp_setup",
    ),
    path(
        "two-factor/backup/tokens/",
        otp_backup,
        name="backup_tokens",
    ),
]
