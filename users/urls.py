from django.urls import path, include

from users.views import EmployeeListView


app_name = "users"
urlpatterns = [path("", EmployeeListView.as_view(), name="employees")]
