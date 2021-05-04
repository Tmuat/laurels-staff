from django.urls import path, include

from home.views import index


urlpatterns = [path("", index, name="home")]
