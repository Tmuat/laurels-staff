import datetime

from regionandhub.models import Hub
from properties.models import PropertyProcess

# python3 manage.py dumpdata > master.json --settings=laurels.settings.production


def delete_surrey():
    property_process_objects = PropertyProcess.objects.all()
    south_west = Hub.objects.get(id="3728fafb-9f16-421a-a727-c494028126ba")

    for instance in property_process_objects:
        if str(instance.hub.id) == "e50a9d9c-80d8-4f06-a75e-14ba42a6af19":
            instance.hub = south_west
            instance.save()


def recent_deals():
    deal_objects = Deal.objects.all()

    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=14)

    for instance in deal_objects:
        if instance.date > seven_days_ago:
            print(instance)

# from common.data_adjust import *
# delete_surrey()