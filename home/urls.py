from django.urls import path

from home.views import (
    index,
    offer_board,
    deal_progression_overview,
    employee_valuation_list,
    employee_instruction_list,
    employee_reduction_list,
    employee_new_business_list,
    add_primary_processor,
    lettings_add_primary_processor,
)


app_name = "home"
urlpatterns = [
    path("", index, name="home"),
    path("properties/offer-board/", offer_board, name="offer_board"),
    path(
        "progression/",
        deal_progression_overview,
        name="deal_progression_overview",
    ),
    path(
        "ajax/valuations/<profile_id>/",
        employee_valuation_list,
        name="employee_valuation_list",
    ),
    path(
        "ajax/instructions/<profile_id>/",
        employee_instruction_list,
        name="employee_instruction_list",
    ),
    path(
        "ajax/reductions/<profile_id>/",
        employee_reduction_list,
        name="employee_reduction_list",
    ),
    path(
        "ajax/new-business/<profile_id>/",
        employee_new_business_list,
        name="employee_new_business_list",
    ),
    path(
        "ajax/primary-progressor/<propertyprocess_id>/",
        add_primary_processor,
        name="add_primary_processor",
    ),
    path(
        "ajax/lettings-primary-progressor/<propertyprocess_id>/",
        lettings_add_primary_processor,
        name="lettings_add_primary_processor",
    ),
]
