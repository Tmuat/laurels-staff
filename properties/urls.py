from django.urls import path

from properties.views import (
    property_list,
    property_detail,
    property_history_pagination,
    property_history_detail,
    offer_history,
    offers_pagination,
    save_property_order,
    property_chain_detail,
    render_property,
    validate_property_address,
    add_property,
    add_propertyprocess,
    add_valuation,
    add_instruction,
    render_history_notes,
    add_history_notes,
    add_reduction,
    add_offerer,
    add_offerer_mortgage,
    add_offerer_cash,
    add_offer,
    add_another_offer,
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
    path(
        "properties/property-chain/new-order/<property_chain_id>/",
        property_chain_detail,
        name="property_chain_detail",
    ),
    path(
        "properties/render/property/",
        render_property,
        name="render_property",
    ),
    path(
        "properties/add/property/",
        add_property,
        name="add_property",
    ),
    path(
        "properties/add/property-process/<property_id>/",
        add_propertyprocess,
        name="add_property_process",
    ),
    path(
        "properties/validate/address/",
        validate_property_address,
        name="validate_property_address",
    ),
    path(
        "properties/add/valuation/<propertyprocess_id>/",
        add_valuation,
        name="add_valuation",
    ),
    path(
        "properties/render/history-notes/<history_id>/",
        render_history_notes,
        name="render_history_notes",
    ),
    path(
        "properties/add/history-notes/<history_id>/",
        add_history_notes,
        name="add_history_notes",
    ),
    path(
        "properties/add/instruction/<propertyprocess_id>/",
        add_instruction,
        name="add_instruction",
    ),
    path(
        "properties/add/reduction/<propertyprocess_id>/",
        add_reduction,
        name="add_reduction",
    ),
    path(
        "properties/add/offerer/<propertyprocess_id>/",
        add_offerer,
        name="add_offerer",
    ),
    path(
        "properties/add/offerer-mortgage/<propertyprocess_id>/<offerer_id>/",
        add_offerer_mortgage,
        name="add_offerer_mortgage",
    ),
    path(
        "properties/add/offerer-cash/<propertyprocess_id>/<offerer_id>/",
        add_offerer_cash,
        name="add_offerer_cash",
    ),
    path(
        "properties/add/offer/<propertyprocess_id>/<offerer_id>/",
        add_offer,
        name="add_offer",
    ),
    path(
        "properties/add/another-offer/<propertyprocess_id>/",
        add_another_offer,
        name="add_another_offer",
    ),
]
