from django.urls import path

from regionandhub.views import (
    hub_and_region,
    region_add,
    validate_region_name,
    hub_add,
    validate_hub_name,
)


app_name = "regionandhub"
urlpatterns = [
    path("manage/", hub_and_region, name="hub_and_region"),
    path("add/region/", region_add, name="add_region"),
    path("check/region/", validate_region_name, name="check_region"),
    path("add/hub/", hub_add, name="add_hub"),
    path("check/hub/", validate_hub_name, name="check_hub"),
]
