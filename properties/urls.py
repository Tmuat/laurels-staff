from django.urls import path

from properties.views import (
    property_list,
    property_detail,
    property_history_pagination,
    property_history_detail,
    offer_history,
    offers_pagination,
    save_property_order
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
        "properties/history/<property_history_id>/",
        property_history_detail,
        name="property_history_instance",
    ),
    path(
        "properties/offers/<propertyprocess_id>/pagination/",
        offers_pagination,
        name="offers_pagination",
    ),
    path(
        "properties/offers/<offerer_id>/",
        offer_history,
        name="offerer_offers",
    ),
    path(
        "properties/property-chain/new-order/",
        save_property_order,
        name="save_property_order",
    ),
]
