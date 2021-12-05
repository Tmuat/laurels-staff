from django.urls import path

from touts.views import (
    area_list,
)


app_name = "touts"
urlpatterns = [
    path("area-list/", area_list, name="area_list"),
]
