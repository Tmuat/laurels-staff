from django.urls import path

from touts.views import (
    area_list,
    tout_list,
    area_add,
    area_edit,
    validate_area_code,
    loud_tout_menu,
    add_tout_property,
    validate_tout_property_address,
    add_landord
)


app_name = "touts"
urlpatterns = [
    path("area-list/", area_list, name="area_list"),
    path("tout-list/", tout_list, name="tout_list"),
    path("area/add/", area_add, name="area_add"),
    path("area/edit/<area_code>/", area_edit, name="area_edit"),
    path("check/area/", validate_area_code, name="validate_area_code"),
    path("tout-list/menu/", loud_tout_menu, name="loud_tout_menu"),
    path(
        "tout-list/add/property/",
        add_tout_property,
        name="add_tout_property"
    ),
    path(
        "tout-list/validate/property/",
        validate_tout_property_address,
        name="validate_tout_property_address"
    ),
    path(
        "tout-list/add/landlord/<tout_property>/",
        add_landord,
        name="add_landord"),
]
