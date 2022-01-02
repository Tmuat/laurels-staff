from django.urls import path

from boards.views import (
    add_board,
    boards_menu,
    board_info
)


app_name = "boards"
urlpatterns = [
    path(
        "boards/add/<board_id>/",
        add_board,
        name="add_board"
    ),
    path(
        "boards/info/<board_id>/",
        board_info,
        name="board_info"
    ),
    path(
        "boards/menu/<board_id>/",
        boards_menu,
        name="boards_menu"
    ),
]
