from django.contrib.auth import views as auth_views
from django.urls import path


from django.contrib.auth.views import LoginView

from accounts.forms import CustomOTPAuthenticationForm
from accounts.views import logout_modal


urlpatterns = [
    path("login/", LoginView.as_view(authentication_form=CustomOTPAuthenticationForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("logout-modal/", logout_modal, name="logout_modal"),
]