from django.urls import path

from regionandhub.views import hub_and_region, region_add, validate_region_name


urlpatterns = [
    path("manage/", hub_and_region, name="hub_and_region"),
    path("add/region/", region_add, name="add_region"),
    path("check/region/", validate_region_name, name="check_region"),
]
