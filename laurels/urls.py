import debug_toolbar

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),

    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path(settings.ADMIN_URL, admin.site.urls),

    path("users/", include("users.urls")),
    path("account/", include("accounts.urls")),
    path("invitation/", include("invitations.urls")),
    path("hub/", include("regionandhub.urls")),
    path("", include("home.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
