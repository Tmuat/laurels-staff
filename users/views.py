from django_otp.decorators import otp_required

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.list import ListView


class EmployeeListView(ListView):

    # model = get_user_model()
    queryset = get_user_model().objects.all()
    paginate_by = 100  # if pagination is desired
    template_name = "users/employee_list_view.html"
