from django.urls import path

from boards.views import add_board


app_name = "boards"
urlpatterns = [
    path(
        "boards/add/<board_id>/",
        add_board,
        name="add_board"
    ),
]
