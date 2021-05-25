from django.urls import path

from properties.views import (
    property_list,
    property_detail,
    property_history_detail,
)


app_name = "properties"
urlpatterns = [
    path("properties/", property_list, name="property_list"),
    path(
        "properties/<propertyprocess_id>/",
        property_detail,
        name="property_list",
    ),
    path(
        "properties/history/<property_history_id>",
        property_history_detail,
        name="property_history_instance",
    ),
]
