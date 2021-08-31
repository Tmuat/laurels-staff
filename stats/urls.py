from django.urls import path

from stats.views import (
    overview,
    more_filters,
    quick_filter_conversion,
    employee_exchanges,
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
]
