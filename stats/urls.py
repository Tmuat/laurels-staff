from django.urls import path

from stats.views import normal_by_person, more_filters, quick_filter_conversion


app_name = "stats"
urlpatterns = [
    path("normal-by-person/", normal_by_person, name="normal_by_person"),
    path("more-filters/", more_filters, name="more_filters"),
    path(
        "quick-filters/",
        quick_filter_conversion,
        name="quick_filter_conversion",
    ),
]
