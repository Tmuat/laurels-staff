from django.urls import path

from stats.views import (
    overview,
    hub_overview,
    more_filters,
    hub_filters,
    quick_filter_conversion,
    employee_exchanges,
    employee_new_business,
    employee_reductions,
    employee_instructions,
    employee_valuations,
    export_overview_xls,
    export_hub_overview_xls,
    export_hub_valuations_xls,
)


app_name = "stats"
urlpatterns = [
    path("overview/", overview, name="overview"),
    path("hub-overview/", hub_overview, name="hub_overview"),
    path("more-filters/", more_filters, name="more_filters"),
    path("hub-filters/", hub_filters, name="hub_filters"),
    path(
        "quick-filters/",
        quick_filter_conversion,
        name="quick_filter_conversion",
    ),
    path(
        "exchanges/<profile_id>/<start_date>/<end_date>/",
        employee_exchanges,
        name="employee_exchanges",
    ),
    path(
        "new-business/<profile_id>/<start_date>/<end_date>/",
        employee_new_business,
        name="employee_new_business",
    ),
    path(
        "reductions/<profile_id>/<start_date>/<end_date>/",
        employee_reductions,
        name="employee_reductions",
    ),
    path(
        "instructions/<profile_id>/<start_date>/<end_date>/",
        employee_instructions,
        name="employee_instructions",
    ),
    path(
        "valuations/<profile_id>/<start_date>/<end_date>/",
        employee_valuations,
        name="employee_valuations",
    ),
    path(
        "export/users/",
        export_overview_xls,
        name="export_overview_xls",
    ),
    path(
        "export/hubs/",
        export_hub_overview_xls,
        name="export_hub_overview_xls",
    ),
    path(
        "export/hub/valuations/<hub_id>/",
        export_hub_valuations_xls,
        name="export_hub_valuations_xls",
    ),
]
