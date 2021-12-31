from django.urls import path

from touts.views import (
    area_list,
    tout_list,
    area_detail,
    area_add,
    area_edit,
    validate_area_code,
    loud_tout_menu,
    add_tout_property,
    validate_tout_property_address,
    add_landord,
    add_landord_existing_property,
    add_marketing,
    add_marketing_existing_landlord,
    tout_info,
    do_not_send,
    show_tout_instances
)


app_name = "touts"
urlpatterns = [
    path("area-list/", area_list, name="area_list"),
    path("tout-list/", tout_list, name="tout_list"),
    path("area-detail/<area_id>/", area_detail, name="area_detail"),
    path("area/add/", area_add, name="area_add"),
    path("area/edit/<area_code>/", area_edit, name="area_edit"),
    path("check/area/", validate_area_code, name="validate_area_code"),
    path("tout-list/menu/", loud_tout_menu, name="loud_tout_menu"),
    path("tout-list/info/<marketing_id>/", tout_info, name="tout_info"),
    path(
        "tout-list/landlord-info/<landlord_id>/",
        show_tout_instances,
        name="show_tout_instances"
    ),
    path(
        "tout-list/do-not-send/<marketing_id>/",
        do_not_send,
        name="do_not_send"
    ),
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
        name="add_landord"
    ),
    path(
        "tout-list/add/landlord/",
        add_landord_existing_property,
        name="add_landord_existing_property"
    ),
    path(
        "tout-list/add/marketing/<landlord>/",
        add_marketing,
        name="add_marketing"
    ),
    path(
        "tout-list/add/marketing/",
        add_marketing_existing_landlord,
        name="add_marketing_existing_landlord"
    ),
]
