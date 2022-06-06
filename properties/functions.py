import logging

from django.shortcuts import get_object_or_404

from properties.models import PropertyProcess, PropertyFeeMaster

logger = logging.getLogger(__name__)

def property_fees_master(propertyprocess_id, fees_instance):
    """
    This function takes in a property fees model instance
    and changes/updates the property_fees master instance for
    the property.

    :param propertyprocess_id - UUID of property process
    :param fees_instance - Instance of property fees model
    :returns - Property Fees Master instance
    """

    propertyprocess = get_object_or_404(
        PropertyProcess,
        id=propertyprocess_id
    )

    property_fee_master = get_object_or_404(
        PropertyFeeMaster,
        propertyprocess=propertyprocess
    )

    property_fee_master.fee = fees_instance.fee
    property_fee_master.price = fees_instance.price
    property_fee_master.new_business = fees_instance.new_business
    property_fee_master.updated_by = fees_instance.updated_by

    property_fee_master.save()

    return property_fee_master
