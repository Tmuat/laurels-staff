import datetime

from lettings.models import Renewals, Gas, EPC, Electrical
from regionandhub.models import Hub
from properties.models import PropertyProcess, Deal, PropertyHistory

# python3 manage.py dumpdata > master.json --settings=laurels.settings.production


def delete_surrey():
    property_process_objects = PropertyProcess.objects.all()
    south_west = Hub.objects.get(id="3728fafb-9f16-421a-a727-c494028126ba")

    for instance in property_process_objects:
        if str(instance.hub.id) == "e50a9d9c-80d8-4f06-a75e-14ba42a6af19":
            instance.hub = south_west
            instance.save()


def delete_deal():
    deal_instance = Deal.objects.get(id="be09cc82-776b-4327-8fe5-3e8138a73cfc")
    deal_instance.delete()


def delete_history():
    history_instance = PropertyHistory.objects.get(id="ba866ad3-3631-4e62-a3db-0bb7ae9c610a")
    history_instance.delete()


def recent_deals():
    deal_objects = Deal.objects.all()

    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=14)

    for instance in deal_objects:
        if instance.date > seven_days_ago:
            print(instance)


def lettings_deal_without_renewal():
    lettings = (
        PropertyProcess.objects.filter(sector="lettings")
        .exclude(macro_status=0)
        .exclude(macro_status=1)
        .exclude(macro_status=2)
        .exclude(macro_status=3)
        .exclude(macro_status=4)
    )

    for instance in lettings:
        if instance.lettings_properties.renewals.first() is None:
            Renewals.objects.create(
                lettings_properties=instance.lettings_properties,
                renewed_on=instance.exchange_and_move.first().exchange_and_move_lettings.move_in_date,
                renewal_date=instance.exchange_and_move.first().exchange_and_move_lettings.first_renewal,
                created=instance.exchange_and_move.first().exchange_and_move_lettings.created,
                created_by=instance.exchange_and_move.first().exchange_and_move_lettings.created_by,
                updated=instance.exchange_and_move.first().exchange_and_move_lettings.updated,
                updated_by=instance.exchange_and_move.first().exchange_and_move_lettings.updated_by,
            )
            # print(instance.exchange_and_move.first().exchange_and_move_lettings.move_in_date)


def lettings_gas():
    lettings = (
        PropertyProcess.objects.filter(sector="lettings")
        .exclude(macro_status=0)
        .exclude(macro_status=1)
        .exclude(macro_status=2)
        .exclude(macro_status=3)
        .exclude(macro_status=4)
    )

    for instance in lettings:
        if (
            instance.lettings_progression.lettings_progression_settings.show_gas
        ):
            if instance.lettings_progression.gas_safety_certificate:
                if instance.lettings_properties.gas.first() is None:
                    Gas.objects.create(
                        lettings_properties=instance.lettings_properties,
                        date=instance.lettings_progression.gas_safety_certificate_date,
                        expiry=instance.lettings_progression.gas_safety_certificate_expiry,
                        created_by=instance.lettings_progression.created_by,
                        updated_by=instance.lettings_progression.updated_by
                    )
                    # print(instance)


def lettings_epc():
    lettings = (
        PropertyProcess.objects.filter(sector="lettings")
        .exclude(macro_status=0)
        .exclude(macro_status=1)
        .exclude(macro_status=2)
        .exclude(macro_status=3)
        .exclude(macro_status=4)
    )

    for instance in lettings:
        if instance.lettings_progression.epc_certificate:
            if instance.lettings_properties.epc.first() is None:
                EPC.objects.create(
                    lettings_properties=instance.lettings_properties,
                    date=instance.lettings_progression.epc_certificate_date,
                    expiry=instance.lettings_progression.epc_certificate_expiry,
                    created_by=instance.lettings_progression.created_by,
                    updated_by=instance.lettings_progression.updated_by
                )
                # print(instance)


def lettings_electrical():
    lettings = (
        PropertyProcess.objects.filter(sector="lettings")
        .exclude(macro_status=0)
        .exclude(macro_status=1)
        .exclude(macro_status=2)
        .exclude(macro_status=3)
        .exclude(macro_status=4)
    )

    for instance in lettings:
        if instance.lettings_progression.electrical_certificate:
            if instance.lettings_properties.electrical.first() is None:
                Electrical.objects.create(
                    lettings_properties=instance.lettings_properties,
                    date=instance.lettings_progression.electrical_certificate_date,
                    expiry=instance.lettings_progression.electrical_certificate_expiry,
                    created_by=instance.lettings_progression.created_by,
                    updated_by=instance.lettings_progression.updated_by
                )


# python manage.py shell
# from common.data_adjust import *
# lettings_deal_without_renewal()
# lettings_gas()
# lettings_epc()
# lettings_electrical()
# delete_deal()
# delete_history()
