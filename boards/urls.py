from django.urls import path

from boards.views import board_modal_controller


app_name = "boards"
urlpatterns = [
    path(
        "boards/controller/<board_id>/",
        board_modal_controller,
        name="board_modal_controller"
    ),
]
