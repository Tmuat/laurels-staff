from django.urls import path

from properties.views import (
    property_list,
    property_detail,
    property_history_pagination,
    property_history_detail,
    offer_history,
    offer_history_lettings,
    offers_pagination,
    notes_pagination,
    save_property_order,
    property_chain_detail,
    render_property,
    validate_property_address,
    add_property,
    add_propertyprocess,
    add_valuation,
    add_instruction,
    add_lettings_instruction,
    render_history_notes,
    add_history_notes,
    add_reduction,
    add_offerer,
    add_offerer_mortgage,
    add_offerer_cash,
    add_offerer_lettings,
    add_offer,
    add_offer_lettings,
    add_another_offer,
    add_another_lettings_offer,
    edit_offerer_cash,
    edit_offerer_mortgage,
    edit_offer_status,
    edit_offer_lettings_status,
    edit_instruction,
    edit_instruction_change,
    withdraw_property,
    back_on_the_market,
    add_deal,
    add_deal_lettings,
    edit_deal,
    add_exchange,
    edit_sales_prog_settings,
    phase_one,
    phase_two,
    phase_three,
    phase_four,
    add_client_info,
    edit_client_info,
    edit_progression_notes,
    add_progression_notes,
    delete_progression_notes,
    add_property_chain_detail,
    edit_property_chain_detail,
    delete_property_chain_detail,
    fall_through,
    manage_sales_progression,
)


app_name = "properties"
urlpatterns = [
    path("properties/", property_list, name="property_list"),
    path(
        "properties/<propertyprocess_id>/",
        property_detail,
        name="property_detail",
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
        "properties/notes/<propertyprocess_id>/pagination/",
        notes_pagination,
        name="notes_pagination",
    ),
    path(
        "properties/offers/<offerer_id>/",
        offer_history,
        name="offerer_offers",
    ),
    path(
        "properties/offers-lettings/<offerer_id>/",
        offer_history_lettings,
        name="offerer_offers_lettings",
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
        "properties/add/property-chain/<propertyprocess_id>/",
        add_property_chain_detail,
        name="add_property_chain_detail",
    ),
    path(
        "properties/edit/property-chain/<property_chain_id>/",
        edit_property_chain_detail,
        name="edit_property_chain_detail",
    ),
    path(
        "properties/delete/property-chain/<property_chain_id>/",
        delete_property_chain_detail,
        name="delete_property_chain_detail",
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
        "properties/add/instruction-lettings/<propertyprocess_id>/",
        add_lettings_instruction,
        name="add_lettings_instruction",
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
        "properties/add/offerer-lettings/<propertyprocess_id>/",
        add_offerer_lettings,
        name="add_offerer_lettings",
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
        "properties/add/offer-lettings/<propertyprocess_id>/<offerer_id>/",
        add_offer_lettings,
        name="add_offer_lettings",
    ),
    path(
        "properties/add/another-offer/<propertyprocess_id>/",
        add_another_offer,
        name="add_another_offer",
    ),
    path(
        "properties/add/another-offer-lettings/<propertyprocess_id>/",
        add_another_lettings_offer,
        name="add_another_lettings_offer",
    ),
    path(
        "properties/edit/offerer-cash/<offerer_id>/",
        edit_offerer_cash,
        name="edit_offerer_cash",
    ),
    path(
        "properties/edit/offerer-mortgage/<offerer_id>/",
        edit_offerer_mortgage,
        name="edit_offerer_mortgage",
    ),
    path(
        "properties/edit/offer-status/<offer_id>/",
        edit_offer_status,
        name="edit_offer_status",
    ),
    path(
        "properties/edit/offer-status-lettings/<offer_id>/",
        edit_offer_lettings_status,
        name="edit_offer_lettings_status",
    ),
    path(
        "properties/edit/instruction/<propertyprocess_id>/",
        edit_instruction,
        name="edit_instruction",
    ),
    path(
        "properties/edit/instruction-change/<instruction_change_id>/",
        edit_instruction_change,
        name="edit_instruction_change",
    ),
    path(
        "properties/withdraw/<propertyprocess_id>/",
        withdraw_property,
        name="withdraw_property",
    ),
    path(
        "properties/back-on-market/<propertyprocess_id>/",
        back_on_the_market,
        name="back_on_the_market",
    ),
    path(
        "properties/add/deal/<propertyprocess_id>/",
        add_deal,
        name="add_deal",
    ),
    path(
        "properties/add/deal-lettings/<propertyprocess_id>/",
        add_deal_lettings,
        name="add_deal_lettings",
    ),
    path(
        "properties/edit/deal/<propertyprocess_id>/",
        edit_deal,
        name="edit_deal",
    ),
    path(
        "properties/add/exchange/<propertyprocess_id>/",
        add_exchange,
        name="add_exchange",
    ),
    path(
        "properties/edit/sales-progression/settings/<propertyprocess_id>/",
        edit_sales_prog_settings,
        name="edit_sales_prog_settings",
    ),
    path(
        "properties/edit/sales-progression/phase-one/<propertyprocess_id>/",
        phase_one,
        name="phase_one",
    ),
    path(
        "properties/edit/sales-progression/phase-two/<propertyprocess_id>/",
        phase_two,
        name="phase_two",
    ),
    path(
        "properties/edit/sales-progression/phase-three/<propertyprocess_id>/",
        phase_three,
        name="phase_three",
    ),
    path(
        "properties/edit/sales-progression/phase-four/<propertyprocess_id>/",
        phase_four,
        name="phase_four",
    ),
    path(
        "properties/add/sales-progression/client-info/<propertyprocess_id>/",
        add_client_info,
        name="add_client_info",
    ),
    path(
        "properties/edit/sales-progression/client-info/<propertyprocess_id>/",
        edit_client_info,
        name="edit_client_info",
    ),
    path(
        "properties/add/sales-progression/notes/<propertyprocess_id>/",
        add_progression_notes,
        name="add_progression_notes",
    ),
    path(
        "properties/edit/sales-progression/notes/<progression_notes_id>/",
        edit_progression_notes,
        name="edit_progression_notes",
    ),
    path(
        "properties/delete/sales-progression/notes/<progression_notes_id>/",
        delete_progression_notes,
        name="delete_progression_notes",
    ),
    path(
        "properties/add/sales-progression/fall-through/<propertyprocess_id>/",
        fall_through,
        name="fall_through",
    ),
    path(
        "properties/manage/sales-progression/<propertyprocess_id>/",
        manage_sales_progression,
        name="manage_sales_progression",
    ),
]
