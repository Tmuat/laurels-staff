from django.urls import path

from stats.views import (
    overview,
    hub_overview,
    extra_stats,
    hub_extra_stats,
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
    export_hub_instructions_xls,
    export_hub_reductions_xls,
    export_hub_new_business_xls,
    export_hub_exchanges_xls,
    pipeline,
    individual_reporting_page,
    get_individual_reporting
)


app_name = "stats"
urlpatterns = [
    path("overview/", overview, name="overview"),
    path("pipeline/", pipeline, name="pipeline"),
    path("hub-overview/", hub_overview, name="hub_overview"),
    path("extra-stats/", extra_stats, name="extra_stats"),
    path("hub-extra-stats/", hub_extra_stats, name="hub_extra_stats"),
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
    path(
        "export/hub/instructions/<hub_id>/",
        export_hub_instructions_xls,
        name="export_hub_instructions_xls",
    ),
    path(
        "export/hub/reductions/<hub_id>/",
        export_hub_reductions_xls,
        name="export_hub_reductions_xls",
    ),
    path(
        "export/hub/new-business/<hub_id>/",
        export_hub_new_business_xls,
        name="export_hub_new_business_xls",
    ),
    path(
        "export/hub/exchanges/<hub_id>/",
        export_hub_exchanges_xls,
        name="export_hub_exchanges_xls",
    ),
    path("individual-reporting/", individual_reporting_page, name="individual_reporting_page"),
    path("get-individual-reporting/", get_individual_reporting, name="get_individual_reporting"),
]
