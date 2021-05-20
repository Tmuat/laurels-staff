import json
import uuid

from django.template.defaultfilters import slugify

# ------------------------------------------------------------------------------
# COMMANDS
# ------------------------------------------------------------------------------

# exec(open('common/data_change.py').read())

# python3 manage.py dumpdata otp_totp.totpdevice > totp.json

# ------------------------------------------------------------------------------
# FUNCITONS
# ------------------------------------------------------------------------------

# unique = []
# non_unique = []

# if instance["fields"]["macro_status"] not in unique:
#         unique.append(instance["fields"]["macro_status"])
#         if instance["fields"]["macro_status"] in non_unique:
#             pass
#         else:
#             non_unique.append(instance["fields"]["macro_status"])


# ------------------------------------------------------------------------------
# DICTIONARIES
# ------------------------------------------------------------------------------

property_dict = None
propertylink_dict = None
hub_dict = None
user_dict = None
profile_dict = None
master_dict = None

# ------------------------------------------------------------------------------
# START SCRIPT
# ------------------------------------------------------------------------------

# ----------------------------------------
# PROPERTY MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/property.json", "r"
) as json_data:
    property_model = json.load(json_data)

for instance in property_model:

    # Changing the model to new value

    instance["model"] = "properties.property"

    # End changing the model to new value

    # Changing the property type to new values

    if instance["fields"]["property_type"] == "House - Terraced":
        instance["fields"]["property_type"] = "house_terraced"

    elif instance["fields"]["property_type"] == "House - End of Terrace":
        instance["fields"]["property_type"] = "house_end_terrace"

    elif instance["fields"]["property_type"] == "House - Semi-Detached":
        instance["fields"]["property_type"] = "house_semi_detached"

    elif instance["fields"]["property_type"] == "House - Detached":
        instance["fields"]["property_type"] = "house_detached"

    elif instance["fields"]["property_type"] == "Maisonette - Ground Floor":
        instance["fields"]["property_type"] = "maisonette_ground_floor"

    elif instance["fields"]["property_type"] == "Maisonette - Top Floor":
        instance["fields"]["property_type"] = "maisonette_top_floor"

    elif instance["fields"]["property_type"] == "Flat - Ground Floor":
        instance["fields"]["property_type"] = "flat_ground_floor"

    elif instance["fields"]["property_type"] == "Flat - Upper Floors":
        instance["fields"]["property_type"] = "flat_upper_floor"

    elif instance["fields"]["property_type"] == "Bungalow - Semi-Detached":
        instance["fields"]["property_type"] = "bungalow_semi_detached"

    elif instance["fields"]["property_type"] == "Bungalow - Detached":
        instance["fields"]["property_type"] = "bungalow_detached"

    elif instance["fields"]["property_type"] == "Commercial":
        instance["fields"]["property_type"] = "commercial"

    elif instance["fields"]["property_type"] == "Land":
        instance["fields"]["property_type"] = "land"

    elif instance["fields"]["property_type"] == "Other":
        instance["fields"]["property_type"] = "other"

    # End change property type

    # Changing the property style to new values

    if instance["fields"]["property_style"] == "Modern":
        instance["fields"]["property_style"] = "modern"

    elif instance["fields"]["property_style"] == "New Build":
        instance["fields"]["property_style"] = "new_build"

    elif instance["fields"]["property_style"] == "Period":
        instance["fields"]["property_style"] = "period"

    # End change property style

    # Changing the property tenure to new values

    if instance["fields"]["tenure"] == "Freehold":
        instance["fields"]["tenure"] = "freehold"

    elif instance["fields"]["tenure"] == "Leasehold":
        instance["fields"]["tenure"] = "leasehold"

    elif instance["fields"]["tenure"] == "Share of Freehold":
        instance["fields"]["tenure"] = "share_of_freehold"

    # End change property tenure

    # Add new fields

    instance["fields"]["created_by"] = "Admin"
    instance["fields"]["created"] = "2000-01-13T13:13:13.000Z"
    instance["fields"]["updated_by"] = "Admin"
    instance["fields"]["updated"] = "2000-01-13T13:13:13.000Z"

    # End add new fields

    # Move original PK

    instance["old_pk"] = instance["pk"]

    # End move original PK

    # Create new UUID field

    instance["pk"] = str(uuid.uuid4())

property_dict = property_model

with open(
    "/workspace/laurels-staff/common/data_dump/property.json", "w"
) as json_data:
    json.dump(property_model, json_data)

# ----------------------------------------
# HUB MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/hub.json", "r"
) as json_data:
    hub_model = json.load(json_data)

for instance in hub_model:

    # Changing the model to new value

    instance["model"] = "regionandhub.hub"

    # End changing the model to new value

    # Add/Update fields

    hub_slug = slugify(instance["fields"]["hub_name"])

    instance["fields"]["slug"] = hub_slug

    instance["fields"]["is_active"] = True

    instance["fields"]["region"] = "aa8b84a7-8cd0-464a-83f1-ceea7b094e73"

    del instance["fields"]["hub_targets"]

    # End Add/Update fields

    # Add new fields

    instance["fields"]["created_by"] = "Admin"
    instance["fields"]["created"] = "2000-01-13T13:13:13.000Z"
    instance["fields"]["updated_by"] = "Admin"
    instance["fields"]["updated"] = "2000-01-13T13:13:13.000Z"

    # End add new fields

    # Move original PK

    instance["old_pk"] = instance["pk"]

    # End move original PK

    # Create new UUID field

    instance["pk"] = str(uuid.uuid4())

hub_dict = hub_model

with open(
    "/workspace/laurels-staff/common/data_dump/hub.json", "w"
) as json_data:
    json.dump(hub_model, json_data)

# ----------------------------------------
# USER PREP
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/profile.json", "r"
) as json_data:
    profile_model = json.load(json_data)

names = []

for instance in profile_model:

    profile_instance = {}

    pk = instance["pk"]

    user_pk = instance["fields"]["user"]

    profile_instance["pk"] = pk

    profile_instance["user_pk"] = user_pk

    name = instance["fields"]["name"]

    if name == "Admin":
        profile_instance["first_name"] = "Admin"
        profile_instance["last_name"] = "User"
    else:
        data = name.split(" ", 1)
        profile_instance["first_name"] = data[0]
        profile_instance["last_name"] = data[1]

    names.append(profile_instance)

# ----------------------------------------
# USER MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/users.json", "r"
) as json_data:
    custom_user_model = json.load(json_data)

for instance in custom_user_model:

    # Changing the model to new value

    instance["model"] = "users.customuser"

    # End changing the model to new value

    # Loop profile list for first name & last name

    first_name = ""
    last_name = ""

    for profile_instance in names:
        if profile_instance["user_pk"] == instance["pk"]:
            first_name = profile_instance["first_name"]
            last_name = profile_instance["last_name"]

    # Add/Update fields

    instance["fields"]["first_name"] = first_name

    instance["fields"]["last_name"] = last_name

    # End Add/Update fields

    # Move original PK

    instance["old_pk"] = instance["pk"]

    # End move original PK

    # Create new UUID field

    instance["pk"] = str(uuid.uuid4())

user_dict = custom_user_model

with open(
    "/workspace/laurels-staff/common/data_dump/users.json", "w"
) as json_data:
    json.dump(custom_user_model, json_data)

# ----------------------------------------
# PROFILE MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/profile.json", "r"
) as json_data:
    profile_model = json.load(json_data)

for instance in profile_model:

    # Changing the model to new value

    instance["model"] = "users.profile"

    # End changing the model to new value

    # Loop user list for one to one link

    for user_instance in user_dict:
        if user_instance["old_pk"] == instance["fields"]["user"]:
            instance["fields"]["user"] = user_instance["pk"]

    # Delete fields

    del instance["fields"]["gender"]

    del instance["fields"]["name"]

    # End Delete fields

    # Link many to many hubs to new PK

    associated_hubs = []

    for hub in instance["fields"]["hub"]:
        for old_hub in hub_dict:
            if hub == old_hub["old_pk"]:
                associated_hubs.append(str(old_hub["pk"]))

    instance["fields"]["hub"] = associated_hubs

    # End link many to many hubs to new PK

    # Edit field name

    instance["fields"]["employee_targets"] = instance["fields"][
        "target_employee"
    ]

    del instance["fields"]["target_employee"]
    del instance["fields"]["target_link"]

    # End edit field name

    # Add new fields

    instance["fields"]["created_by"] = "Admin"
    instance["fields"]["created"] = "2000-01-13T13:13:13.000Z"
    instance["fields"]["updated_by"] = "Admin"
    instance["fields"]["updated"] = "2000-01-13T13:13:13.000Z"

    # End add new fields

    # Move original PK

    instance["old_pk"] = instance["pk"]

    # End move original PK

    # Create new UUID field

    instance["pk"] = str(uuid.uuid4())

profile_dict = profile_model

with open(
    "/workspace/laurels-staff/common/data_dump/profile.json", "w"
) as json_data:
    json.dump(profile_model, json_data)


# ----------------------------------------
# PROPERTY LINK MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/property_process.json", "r"
) as json_data:
    property_link_model = json.load(json_data)

for instance in property_link_model:

    # Changing the model to new value

    instance["model"] = "properties.propertylink"

    # End changing the model to new value

    # Changing the macro_status to new values

    if instance["fields"]["macro_status"] == "Valuation":
        instance["fields"]["macro_status"] = "valuation"

    elif instance["fields"]["macro_status"] == "Instruction":
        instance["fields"]["macro_status"] = "instruction"

    elif instance["fields"]["macro_status"] == "Viewing":
        instance["fields"]["macro_status"] = "viewing"

    elif instance["fields"]["macro_status"] == "Deal":
        instance["fields"]["macro_status"] = "deal"

    elif instance["fields"]["macro_status"] == "Complete":
        instance["fields"]["macro_status"] = "complete"

    elif instance["fields"]["macro_status"] == "Withdrawn":
        instance["fields"]["macro_status"] = "withdrawn"

    # End change macro_status

    # Changing the sector to new values

    if instance["fields"]["sector"] == "Sales":
        instance["fields"]["sector"] = "sales"

    elif instance["fields"]["sector"] == "Lettings":
        instance["fields"]["sector"] = "lettings"
    
    # End sector change

    # Loop property list for property link & delete old field

    for property_instance in property_dict:
        if property_instance["old_pk"] == instance["fields"]["property_link"]:
            instance["fields"]["property"] = property_instance["pk"]

    del instance["fields"]["property_link"]

    # End loop

    # Loop profile list for employee link & delete old field

    for profile_instance in profile_dict:
        if profile_instance["old_pk"] == instance["fields"]["employee_link"]:
            instance["fields"]["employee"] = profile_instance["pk"]

    del instance["fields"]["employee_link"]

    # End loop

    # Loop hub list for employee link & delete old field

    for hub_instance in hub_dict:
        if hub_instance["old_pk"] == instance["fields"]["static_hub"]:
            instance["fields"]["hub"] = hub_instance["pk"]

    del instance["fields"]["static_hub"]

    # End loop

    # Add new fields

    instance["fields"]["created_by"] = "Admin"
    instance["fields"]["created"] = "2000-01-13T13:13:13.000Z"
    instance["fields"]["updated_by"] = "Admin"
    instance["fields"]["updated"] = "2000-01-13T13:13:13.000Z"

    # End add new fields

    # Move original PK

    instance["old_pk"] = instance["pk"]

    # End move original PK

    # Create new UUID field

    instance["pk"] = str(uuid.uuid4())

propertylink_dict = property_link_model

with open(
    "/workspace/laurels-staff/common/data_dump/property_link.json", "w"
) as json_data:
    json.dump(property_link_model, json_data)


# ----------------------------------------
# CREATE MASTER JSON
# ----------------------------------------

master_dict = []

for object in hub_dict:
    master_dict.append(object)

for object in user_dict:
    master_dict.append(object)

for object in profile_dict:
    master_dict.append(object)

for object in property_dict:
    master_dict.append(object)

for object in propertylink_dict:
    master_dict.append(object)

with open(
    "/workspace/laurels-staff/common/data_dump/master.json", "w"
) as json_data:
    json.dump(master_dict, json_data)
