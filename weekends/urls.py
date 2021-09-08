from django.urls import path

from weekends.views import (
    weekend_working,
    weekend_working_json,
    add_weekend_working,
    delete_weekend_working,
)


app_name = "weekends"
urlpatterns = [
    path("weekend-working/", weekend_working, name="weekend_working"),
    path(
        "ajax/weekend-working/<hub_slug>/",
        weekend_working_json,
        name="weekend_working_json",
    ),
    path(
        "ajax/add-weekend-working/",
        add_weekend_working,
        name="add_weekend_working",
    ),
    path(
        "ajax/delete-weekend-working/",
        delete_weekend_working,
        name="delete_weekend_working",
    ),
]
