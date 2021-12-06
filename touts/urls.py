from django.urls import path

from touts.views import (
    area_list,
    tout_list,
    area_add,
    area_edit,
    validate_area_code,
)


app_name = "touts"
urlpatterns = [
    path("area-list/", area_list, name="area_list"),
    path("tout-list/", tout_list, name="tout_list"),
    path("area/add/", area_add, name="area_add"),
    path("area/edit/<area_code>/", area_edit, name="area_edit"),
    path("check/area/", validate_area_code, name="validate_area_code"),
]
