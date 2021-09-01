from django.urls import path

from stats.views import (
    overview,
    more_filters,
    quick_filter_conversion,
    employee_exchanges,
    employee_new_business,
    employee_reductions,
)


app_name = "stats"
urlpatterns = [
    path("overview/", overview, name="overview"),
    path("more-filters/", more_filters, name="more_filters"),
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
]
