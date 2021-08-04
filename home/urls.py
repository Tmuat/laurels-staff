from django.urls import path

from home.views import index, offer_board


app_name = "home"
urlpatterns = [
    path("", index, name="home"),
    path("properties/offer-board/", offer_board, name="offer_board"),
]
