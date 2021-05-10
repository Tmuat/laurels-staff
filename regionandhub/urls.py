from django.urls import path, include

from regionandhub.views import hub_and_region


urlpatterns = [path("manage/", hub_and_region, name="hub_and_region")]
