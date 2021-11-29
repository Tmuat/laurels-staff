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
    path("users/invitations/", include("invitations.urls")),
    path("region-hub/", include("regionandhub.urls")),
    path("", include("home.urls")),
    path("", include("properties.urls")),
    path("lettings/", include("lettings.urls")),
    path("", include("weekends.urls")),
    path("statistics/", include("stats.urls")),
    path("support/", include("support.urls")),
    path("boards/", include("boards.urls")),
    path("touting/", include("touts.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
