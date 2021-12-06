from django.urls import path

from touts.views import (
    area_list,
    area_add,
    validate_area_code,
)


app_name = "touts"
urlpatterns = [
    path("area-list/", area_list, name="area_list"),
    path("area/add/", area_add, name="area_add"),
    path("check/area/", validate_area_code, name="validate_area_code"),
]
