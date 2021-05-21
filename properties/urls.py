from django.urls import path

from properties.views import property_list


app_name = "properties"
urlpatterns = [path("properties/", property_list, name="property_list")]
