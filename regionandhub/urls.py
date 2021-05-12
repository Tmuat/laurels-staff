from django.urls import path

from regionandhub.views import (
    hub_and_region,
    region_add,
    validate_region_name,
    region_edit,
    validate_region_name_edit,
    check_region_hubs,
    hub_add,
    validate_hub_name,
    hub_add_targets,
)


app_name = "regionandhub"
urlpatterns = [
    path("manage/", hub_and_region, name="hub_and_region"),
    path("add/region/", region_add, name="add_region"),
    path("check/region/", validate_region_name, name="check_region"),
    path("edit/region/<region_slug>/", region_edit, name="edit_region"),
    path(
        "check/region/<region_slug>/",
        validate_region_name_edit,
        name="check_region_edit",
    ),
    path(
        "check/region/hubs/<region_slug>/",
        check_region_hubs,
        name="check_region_hubs",
    ),
    path("add/hub/", hub_add, name="add_hub"),
    path("check/hub/", validate_hub_name, name="check_hub"),
    path("add/<hub>/hub-targets/", hub_add_targets, name="add_hub_targets"),
]
