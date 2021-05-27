from django.urls import path

from properties.views import (
    property_list,
    property_detail,
    property_history_pagination,
    property_history_detail,
    offer_history,
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
        "properties/history/<propertyprocess_id>/pagination/",
        property_history_pagination,
        name="property_history_pagination",
    ),
    path(
        "properties/history/<property_history_id>",
        property_history_detail,
        name="property_history_instance",
    ),
    path(
        "properties/offers/<offerer_id>",
        offer_history,
        name="offerer_offers",
    ),
]
