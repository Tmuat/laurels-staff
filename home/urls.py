from django.urls import path

from home.views import (
    index,
    offer_board,
    progression_overview,
    employee_valuation_list,
    employee_instruction_list,
    employee_reduction_list,
    employee_new_business_list,
)


app_name = "home"
urlpatterns = [
    path("", index, name="home"),
    path("properties/offer-board/", offer_board, name="offer_board"),
    path("properties/progression-overview/", progression_overview, name="progression_overview"),
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
]
