import datetime

from lettings.models import Renewals, Gas, EPC, Electrical
from regionandhub.models import Hub
from properties.models import PropertyProcess, Deal, PropertyHistory, Offer, Reduction, PropertyFees, PropertyFeeMaster, Marketing

# python3 manage.py dumpdata > master.json --settings=laurels.settings.production


def adjust_property_fee_date():
    property_fee = PropertyFees.objects.get(
        id="ea626962-f0e5-40b4-b588-81ff729d266d"
    )
    property_fee.date = "2021-01-28"
    property_fee.save()

    property_fee = PropertyFees.objects.get(
        id="ffd9af53-ba52-4f1b-b63e-ae6fa2eca5a9"
    )
    property_fee.date = "2021-02-26"
    property_fee.save()

    property_fee = PropertyFees.objects.get(
        id="c6c6f8f1-3244-4389-a9cf-ceb0a3dccd1f"
    )
    property_fee.date = "2021-02-09"
    property_fee.save()

    property_fee = PropertyFees.objects.get(
        id="4bbd94e2-bbd9-4ffe-a780-01d153095d91"
    )
    property_fee.date = "2021-02-12"
    property_fee.save()

    property_fee = PropertyFees.objects.get(
        id="49d5affa-a079-434a-988e-df265ab69b78"
    )
    property_fee.date = "2021-04-29"
    property_fee.save()

    property_fee = PropertyFees.objects.get(
        id="a99b8d6f-ee46-4df8-8b9c-8db9d1dcd3fe"
    )
    property_fee.date = "2021-04-17"
    property_fee.save()

    pp = PropertyProcess.objects.get(
        id="efecdd4f-f2ea-45a9-b2b3-de56698d2430"
    )

    PropertyFees.objects.create(
        propertyprocess=pp,
        fee=6,
        price=1350,
        date="2021-03-17",
        created_by="Automated",
        updated_by="Automated"
    )

    pp = PropertyProcess.objects.get(
        id="2b5512e6-0245-448b-ac26-bca72af04083"
    )

    PropertyFees.objects.create(
        propertyprocess=pp,
        fee=0.85,
        price=375000,
        date="2021-08-05",
        created_by="Automated",
        updated_by="Automated"
    )


def change_fee():
    pf = PropertyFeeMaster.objects.get(
        id="b36501d3-e1cb-42dc-a584-2f5d455e544b"
    )
    pf.price = 350000
    pf.new_business = 2800
    pf.save()


def property_fee_master():
    pp = PropertyProcess.objects.exclude(
        macro_status=1
    ).exclude(
        macro_status=2
    )
    adjust_property_fee_date()
    for p in pp:
        if p.property_fees.exists():
            if p.macro_status == 0:
                PropertyFeeMaster.objects.create(
                    propertyprocess=p,
                    fee=p.property_fees.first().fee,
                    price=p.property_fees.first().price,
                    new_business=p.property_fees.first().new_business,
                    created_by="Automated",
                    updated_by="Automated",
                )
                # pass
            else:
                if p.property_fees.first().fee < 0:
                    if p.previously_fallen_through is True:
                        print(p)
                        PropertyFeeMaster.objects.create(
                            propertyprocess=p,
                            fee=p.property_fees.first().fee,
                            price=p.property_fees.first().price,
                            new_business=p.property_fees.first().new_business,
                            created_by="Automated",
                            updated_by="Automated",
                        )
                        # pass
                    else:
                        PropertyFeeMaster.objects.create(
                            propertyprocess=p,
                            fee=p.property_fees.first().fee,
                            price=p.property_fees.first().price,
                            new_business=p.property_fees.first().new_business,
                            created_by="Automated",
                            updated_by="Automated",
                        )
                        # pass
                else:
                    PropertyFeeMaster.objects.create(
                        propertyprocess=p,
                        fee=p.property_fees.first().fee,
                        price=p.property_fees.first().price,
                        new_business=p.property_fees.first().new_business,
                        created_by="Automated",
                        updated_by="Automated",
                    )
                    # pass


def check_pp_deal():
    property_process_objects = PropertyProcess.objects.filter(
        macro_status=3
    )
    for instance in property_process_objects:
        pp = PropertyProcess.objects.get(id=instance.id)
        if Deal.objects.filter(propertyprocess=pp).exists():
            print(instance)


def delete_surrey():
    property_process_objects = PropertyProcess.objects.all()
    south_west = Hub.objects.get(id="3728fafb-9f16-421a-a727-c494028126ba")

    for instance in property_process_objects:
        if str(instance.hub.id) == "e50a9d9c-80d8-4f06-a75e-14ba42a6af19":
            instance.hub = south_west
            instance.save()


def delete_deal():
    deal_instance = Deal.objects.get(id="c3789d6b-0df7-4f8e-bd22-b68830a8caf6")
    deal_instance.delete()
    print("Deleted")


def create_deal():
    pp = PropertyProcess.objects.get(id="f7d1f0e9-e437-4ef7-b99e-f0d48d6d89b8")
    offer = Offer.objects.get(id="aa406fd0-fb42-42a1-8e46-a9f268faa5e0")
    Deal.objects.create(
        propertyprocess=pp,
        date="2022-01-19",
        target_move_date="2022-01-19",
        offer_accepted=offer,
        created_by="Matthew Gabre-Kristos",
        updated_by="Matthew Gabre-Kristos"
    )
    print("Created")


def delete_history():
    history_instance = PropertyHistory.objects.get(
        id="91bec0e3-2055-4034-9370-222dc0dfeeb4"
    )
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
                        updated_by=instance.lettings_progression.updated_by,
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
                    updated_by=instance.lettings_progression.updated_by,
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
                    updated_by=instance.lettings_progression.updated_by,
                )


def deal_agreed_change():
    deal = Deal.objects.get(id="50ef6738-37eb-44f7-9970-0f7ed81bee7a")
    offer = Offer.objects.get(id="476e5ed9-90bf-4f00-9347-540176643790")
    deal.offer_accepted = offer
    deal.save()
    print(deal.offer_accepted)
    print("Saved")


def delete_reduction():
    reduction_instance = Reduction.objects.get(id="4b7c0c30-884f-4f0f-a0ce-a217a7b7ebaa")
    reduction_instance.delete()
    print("Deleted")


def delete_prop_fee():
    fee_instance = PropertyFees.objects.get(id="698cb8fa-ccb7-4eb0-babe-cd2bf9fd26c0")
    fee_instance.delete()
    print("Deleted")


def marketing_info():
    marketing_instance = Marketing.objects.all()
    for instance in marketing_instance:
        if instance.hear_about_laurels == "google_search":
            instance.hear_about_laurels = Marketing.WEBSEARCH
            instance.save()
        elif instance.hear_about_laurels == "marketing_boards":
            instance.hear_about_laurels = Marketing.BOARDS
            instance.save()
        elif instance.hear_about_laurels == "sold_let_flyer":
            instance.hear_about_laurels = Marketing.PRINTDROP
            instance.save()
        elif instance.hear_about_laurels == "tout_letter":
            instance.hear_about_laurels = Marketing.PRINTDROP
            instance.save()
        elif instance.hear_about_laurels == "specific_letter":
            instance.hear_about_laurels = Marketing.PRINTDROP
            instance.save()
        elif instance.hear_about_laurels == "brochure":
            instance.hear_about_laurels = Marketing.PRINTDROP
            instance.save()
        elif instance.hear_about_laurels == "business_card_drop":
            instance.hear_about_laurels = Marketing.PRINTDROP
            instance.save()
        elif instance.hear_about_laurels == "combined_touting":
            instance.hear_about_laurels = Marketing.PRINTDROP
            instance.save()


# python manage.py shell --settings=laurels.settings.production
# from common.data_adjust import *
# lettings_deal_without_renewal()
# lettings_gas()
# lettings_epc()
# lettings_electrical()
# delete_deal()
# delete_history()
# deal_agreed_change()
# delete_reduction()
# delete_prop_fee()
# property_fee_master()
