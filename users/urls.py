from django.urls import path

from users.views import (
    employees,
    add_user_targets,
    edit_user_targets,
    user_detail,
    edit_user,
)


app_name = "users"
urlpatterns = [
    path("", employees, name="employees"),
    path(
        "add/user-targets/<user>/<year>",
        add_user_targets,
        name="add_user_targets"
    ),
    path(
        "edit/user-targets/<user>/<year>",
        edit_user_targets,
        name="edit_user_targets"
    ),
    path(
        "view/user/<user>/",
        user_detail,
        name="user_detail"
    ),
    path(
        "edit/user/<user>/",
        edit_user,
        name="edit_user"
    )
]
