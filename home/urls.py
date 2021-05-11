from django.urls import path, include

from home.views import index


app_name = "home"
urlpatterns = [path("", index, name="home")]
