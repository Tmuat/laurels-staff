from django.urls import path, include

from home.views import index, offer_board


app_name = "home"
urlpatterns = [
    path("", index, name="home"),
    path("properties/offer-board/", offer_board, name="offer_board")]
