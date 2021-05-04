from django.contrib.auth import views as auth_views
from django.urls import path, include

from accounts.views import logout_modal


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('logout-modal/', logout_modal, name="logout_modal"),
]
