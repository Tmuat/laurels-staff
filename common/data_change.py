import json
import uuid

from django.template.defaultfilters import slugify

# ------------------------------------------------------------------------------
# COMMANDS
# ------------------------------------------------------------------------------

# python3 manage.py shell

# exec(open('common/data_change.py').read())

# python3 manage.py dumpdata home.valuation > valuations.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.propertyprocess > property_process.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata otp_totp.totpdevice > totp.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.property > property.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.instruction > instruction.json --settings=laurels_staff_portal.settings.production

# python3 manage.py loaddata master.json

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

setup_dict = None
super_dict = None
property_dict = None
propertyprocess_dict = None
property_history_dict = None
valuation_dict = None
instruction_dict = None
instruction_lettings_extra_dict = None
hub_dict = None
hub_targets_dict = None
user_dict = None
totp_dict = None
profile_dict = None
master_dict = None

# ------------------------------------------------------------------------------
# START SCRIPT
# ------------------------------------------------------------------------------

# ----------------------------------------
# SETUP
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/setup.json", "r"
) as json_data:
    setup = json.load(json_data)

setup_dict = setup

with open(
    "/workspace/laurels-staff/common/data_dump/originals/superuser.json", "r"
) as json_data:
    super = json.load(json_data)

super_dict = super

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

    instance["hub_targets_link"] = instance["fields"]["hub_targets"]

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
# HUB TARGETS MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/hubtargets.json", "r"
) as json_data:
    hub_targets_model = json.load(json_data)

hub_targets = []

for instance in hub_targets_model:

    q1_2021 = {}
    q2_2021 = {}
    q3_2021 = {}
    q4_2021 = {}

    q1_2021_fields = {}
    q2_2021_fields = {}
    q3_2021_fields = {}
    q4_2021_fields = {}

    hub_targets_year = {}
    hub_targets_year_fields = {}

    # Changing the model to new value

    q1_2021["model"] = "regionandhub.hubtargets"
    q2_2021["model"] = "regionandhub.hubtargets"
    q3_2021["model"] = "regionandhub.hubtargets"
    q4_2021["model"] = "regionandhub.hubtargets"

    hub_targets_year["model"] = "regionandhub.hubtargetsyear"

    # End changing the model to new value

    # Create pk for new instances

    q1_2021["pk"] = str(uuid.uuid4())
    q2_2021["pk"] = str(uuid.uuid4())
    q3_2021["pk"] = str(uuid.uuid4())
    q4_2021["pk"] = str(uuid.uuid4())

    hub_targets_year["pk"] = str(uuid.uuid4())

    # End creating new instances

    # Adding year & quarter for new instances

    q1_2021_fields["year"] = "2021"
    q2_2021_fields["year"] = "2021"
    q3_2021_fields["year"] = "2021"
    q4_2021_fields["year"] = "2021"

    hub_targets_year_fields["year"] = "2021"

    q1_2021_fields["quarter"] = "q1"
    q2_2021_fields["quarter"] = "q2"
    q3_2021_fields["quarter"] = "q3"
    q4_2021_fields["quarter"] = "q4"

    # End adding year & quarter new instances

    # Adding hub link

    for hub_instance in hub_dict:
        if hub_instance["hub_targets_link"] == instance["pk"]:

            q1_2021_fields["hub_targets"] = hub_instance["pk"]
            q2_2021_fields["hub_targets"] = hub_instance["pk"]
            q3_2021_fields["hub_targets"] = hub_instance["pk"]
            q4_2021_fields["hub_targets"] = hub_instance["pk"]

            hub_targets_year_fields["hub"] = hub_instance["pk"]

    # End hub link

    # Set hub targets to true

    hub_targets_year_fields["targets_set"] = True

    # End set hub targets to true

    # Update fields

    q1_2021_fields["instructions"] = instance["fields"][
        "q1_2021_instructions_hub"
    ]
    q2_2021_fields["instructions"] = instance["fields"][
        "q2_2021_instructions_hub"
    ]
    q3_2021_fields["instructions"] = instance["fields"][
        "q3_2021_instructions_hub"
    ]
    q4_2021_fields["instructions"] = instance["fields"][
        "q4_2021_instructions_hub"
    ]

    q1_2021_fields["reductions"] = instance["fields"]["q1_2021_reductions_hub"]
    q2_2021_fields["reductions"] = instance["fields"]["q2_2021_reductions_hub"]
    q3_2021_fields["reductions"] = instance["fields"]["q3_2021_reductions_hub"]
    q4_2021_fields["reductions"] = instance["fields"]["q4_2021_reductions_hub"]

    q1_2021_fields["new_business"] = instance["fields"][
        "q1_2021_new_business_hub"
    ]
    q2_2021_fields["new_business"] = instance["fields"][
        "q2_2021_new_business_hub"
    ]
    q3_2021_fields["new_business"] = instance["fields"][
        "q3_2021_new_business_hub"
    ]
    q4_2021_fields["new_business"] = instance["fields"][
        "q4_2021_new_business_hub"
    ]

    q1_2021_fields["exchange_and_move"] = instance["fields"][
        "q1_2021_exchange_and_move_hub"
    ]
    q2_2021_fields["exchange_and_move"] = instance["fields"][
        "q2_2021_exchange_and_move_hub"
    ]
    q3_2021_fields["exchange_and_move"] = instance["fields"][
        "q3_2021_exchange_and_move_hub"
    ]
    q4_2021_fields["exchange_and_move"] = instance["fields"][
        "q4_2021_exchange_and_move_hub"
    ]

    # End Update fields

    # Add new fields

    q1_2021_fields["created_by"] = "Admin"
    q1_2021_fields["created"] = "2000-01-13T13:13:13.000Z"
    q1_2021_fields["updated_by"] = "Admin"
    q1_2021_fields["updated"] = "2000-01-13T13:13:13.000Z"

    q2_2021_fields["created_by"] = "Admin"
    q2_2021_fields["created"] = "2000-01-13T13:13:13.000Z"
    q2_2021_fields["updated_by"] = "Admin"
    q2_2021_fields["updated"] = "2000-01-13T13:13:13.000Z"

    q3_2021_fields["created_by"] = "Admin"
    q3_2021_fields["created"] = "2000-01-13T13:13:13.000Z"
    q3_2021_fields["updated_by"] = "Admin"
    q3_2021_fields["updated"] = "2000-01-13T13:13:13.000Z"

    q4_2021_fields["created_by"] = "Admin"
    q4_2021_fields["created"] = "2000-01-13T13:13:13.000Z"
    q4_2021_fields["updated_by"] = "Admin"
    q4_2021_fields["updated"] = "2000-01-13T13:13:13.000Z"

    hub_targets_year_fields["created_by"] = "Admin"
    hub_targets_year_fields["created"] = "2000-01-13T13:13:13.000Z"
    hub_targets_year_fields["updated_by"] = "Admin"
    hub_targets_year_fields["updated"] = "2000-01-13T13:13:13.000Z"

    # End add new fields

    # Add fields to larger dict

    q1_2021["fields"] = q1_2021_fields
    q2_2021["fields"] = q2_2021_fields
    q3_2021["fields"] = q3_2021_fields
    q4_2021["fields"] = q4_2021_fields

    hub_targets_year["fields"] = hub_targets_year_fields

    # End adding fields to larger dict

    # Add to dict

    hub_targets.append(q1_2021)
    hub_targets.append(q2_2021)
    hub_targets.append(q3_2021)
    hub_targets.append(q4_2021)
    hub_targets.append(hub_targets_year)

hub_targets_dict = hub_targets

with open(
    "/workspace/laurels-staff/common/data_dump/hubtargets.json", "w"
) as json_data:
    json.dump(hub_targets, json_data)

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

    # Edit field names

    instance["fields"]["employee_targets"] = instance["fields"][
        "target_employee"
    ]

    instance["fields"]["personal_comm"] = instance["fields"]["p_comm"]

    instance["fields"]["office_comm"] = instance["fields"]["o_comm"]

    del instance["fields"]["target_employee"]
    del instance["fields"]["target_link"]
    del instance["fields"]["p_comm"]
    del instance["fields"]["o_comm"]

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
# TOTP MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/totp.json",
    "r",
) as json_data:
    totp_model = json.load(json_data)

for instance in totp_model:

    # Loop profile list for employee link & delete old field

    for user_instance in user_dict:
        if user_instance["old_pk"] == instance["fields"]["user"]:
            instance["fields"]["user"] = user_instance["pk"]

    # End loop

totp_dict = totp_model

with open(
    "/workspace/laurels-staff/common/data_dump/totp.json", "w"
) as json_data:
    json.dump(totp_model, json_data)


# ----------------------------------------
# PROPERTY PROCESS MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/property_process.json",
    "r",
) as json_data:
    property_process_model = json.load(json_data)

for instance in property_process_model:

    # Changing the model to new value

    instance["model"] = "properties.propertyprocess"

    # End changing the model to new value

    # Changing the macro_status to new values

    if instance["fields"]["macro_status"] == "Valuation":
        instance["fields"]["macro_status"] = "val"

    elif instance["fields"]["macro_status"] == "Instruction":
        instance["fields"]["macro_status"] = "inst"

    elif instance["fields"]["macro_status"] == "Viewing":
        instance["fields"]["macro_status"] = "view"

    elif instance["fields"]["macro_status"] == "Deal":
        instance["fields"]["macro_status"] = "deal"

    elif instance["fields"]["macro_status"] == "Complete":
        instance["fields"]["macro_status"] = "comp"

    elif instance["fields"]["macro_status"] == "Withdrawn":
        instance["fields"]["macro_status"] = "withd"

    # End change macro_status

    # Changing the sector to new values

    if instance["fields"]["sector"] == "Sales":
        instance["fields"]["sector"] = "sales"

    elif instance["fields"]["sector"] == "Lettings":
        instance["fields"]["sector"] = "lettings"

    # End sector change

    # Loop property list for property process & delete old field

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

propertyprocess_dict = property_process_model

with open(
    "/workspace/laurels-staff/common/data_dump/property_link.json", "w"
) as json_data:
    json.dump(property_process_model, json_data)


# ----------------------------------------
# PROPERTY HISTORY MODEL
# ----------------------------------------

history = []

for instance in propertyprocess_dict:

    property_history = {}
    property_history_fields = {}

    # Changing the model to new value

    property_history["model"] = "properties.propertyhistory"

    # Create new UUID field

    property_history["pk"] = str(uuid.uuid4())

    # End new UUID

    # Add propertyprocess link

    property_history_fields["propertyprocess"] = instance["pk"]

    # End add propertyprocess link

    # Add new fields

    property_history_fields["type"] = "other"

    if instance["fields"]["sector"] == "sales":
        property_history_fields[
            "description"
        ] = "There is no history for this Property Sale"
    else:
        property_history_fields[
            "description"
        ] = "There is no history for this Property Letting"

    property_history_fields["created_by"] = "Admin"
    property_history_fields["created"] = "2000-01-13T13:13:13.000Z"
    property_history_fields["updated_by"] = "Admin"
    property_history_fields["updated"] = "2000-01-13T13:13:13.000Z"

    # End add new fields

    property_history["fields"] = property_history_fields

    history.append(property_history)

property_history_dict = history

with open(
    "/workspace/laurels-staff/common/data_dump/property_history.json", "w"
) as json_data:
    json.dump(history, json_data)


# ----------------------------------------
# VALUATION MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/valuation.json",
    "r",
) as json_data:
    valuation_model = json.load(json_data)

for instance in valuation_model:

    # Changing the model to new value

    instance["model"] = "properties.valuation"

    # End changing the model to new value

    # Loop property list for property process & delete old field

    for propertyprocess_instance in propertyprocess_dict:
        if (
            propertyprocess_instance["old_pk"]
            == instance["fields"]["propertyprocess_link"]
        ):
            instance["fields"]["propertyprocess"] = propertyprocess_instance[
                "pk"
            ]

    del instance["fields"]["propertyprocess_link"]

    # End loop

    # Add new fields

    instance["fields"]["created_by"] = "Admin"
    instance["fields"]["created"] = "2000-01-13T13:13:13.000Z"
    instance["fields"]["updated_by"] = "Admin"
    instance["fields"]["updated"] = "2000-01-13T13:13:13.000Z"

    # End add new fields

    # Delete old field

    del instance["fields"]["employee_valuer"]

    # End delete

    # Move original PK

    instance["old_pk"] = instance["pk"]

    # End move original PK

    # Create new UUID field

    instance["pk"] = str(uuid.uuid4())

valuation_dict = valuation_model

with open(
    "/workspace/laurels-staff/common/data_dump/valuation.json", "w"
) as json_data:
    json.dump(valuation_model, json_data)


# ----------------------------------------
# INSTRUCTION MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/instruction.json",
    "r",
) as json_data:
    instruction_model = json.load(json_data)

instruction_extra_dict = []

for instance in instruction_model:

    instruction_extra = {}
    instruction_extra_fields = {}

    # Changing the model to new value

    instance["model"] = "properties.instruction"
    instruction_extra["model"] = "properties.instructionlettingsextra"

    # End changing the model to new value

    # Loop property list for property process & delete old field

    for propertyprocess_instance in propertyprocess_dict:
        if (
            propertyprocess_instance["old_pk"]
            == instance["fields"]["propertyprocess_link"]
        ):
            instance["fields"]["propertyprocess"] = propertyprocess_instance[
                "pk"
            ]
            instruction_extra_fields[
                "propertyprocess"
            ] = propertyprocess_instance["pk"]

    del instance["fields"]["propertyprocess_link"]

    # End loop

    # Changing the agreement_type to new values

    if instance["fields"]["agreement_type"] == "Sole":
        instance["fields"]["agreement_type"] = "sole"

    elif instance["fields"]["agreement_type"] == "Mutli":
        instance["fields"]["agreement_type"] = "multi"

    # End change agreement_type

    # Changing the length_of_contract to new values

    if instance["fields"]["length_of_contract"] == "16 Weeks":
        instance["fields"]["length_of_contract"] = 16

    elif instance["fields"]["length_of_contract"] == "12 Weeks":
        instance["fields"]["length_of_contract"] = 12

    elif instance["fields"]["length_of_contract"] == "10 Weeks":
        instance["fields"]["length_of_contract"] = 10

    elif instance["fields"]["length_of_contract"] == "8 Weeks":
        instance["fields"]["length_of_contract"] = 8

    elif instance["fields"]["length_of_contract"] == "6 Weeks":
        instance["fields"]["length_of_contract"] = 6

    elif instance["fields"]["length_of_contract"] == "4 Weeks (Multi Only)":
        instance["fields"]["length_of_contract"] = 4

    # End change length_of_contract

    # Add fields to new model

    if instance["fields"]["lettings_service_level"] == "Intro Only":
        instruction_extra_fields["lettings_service_level"] = "intro_only"

    elif instance["fields"]["lettings_service_level"] == "Rent Collect":
        instruction_extra_fields["lettings_service_level"] = "rent_collect"

    elif instance["fields"]["lettings_service_level"] == "Fully Managed":
        instruction_extra_fields["lettings_service_level"] = "fully_managed"

    elif (
        instance["fields"]["lettings_service_level"]
        == "Fully Managed Rent Insurance Included"
    ):
        instruction_extra_fields["lettings_service_level"] = "fully_managed_ri"

    instruction_extra_fields["managed_property"] = instance["fields"][
        "managed_property"
    ]

    del instance["fields"]["lettings_service_level"]
    del instance["fields"]["managed_property"]

    # End add fields to new model

    # Add new fields

    instance["fields"]["created_by"] = "Admin"
    instance["fields"]["created"] = "2000-01-13T13:13:13.000Z"
    instance["fields"]["updated_by"] = "Admin"
    instance["fields"]["updated"] = "2000-01-13T13:13:13.000Z"

    instruction_extra_fields["created_by"] = "Admin"
    instruction_extra_fields["created"] = "2000-01-13T13:13:13.000Z"
    instruction_extra_fields["updated_by"] = "Admin"
    instruction_extra_fields["updated"] = "2000-01-13T13:13:13.000Z"

    # End add new fields

    # Move original PK

    instance["old_pk"] = instance["pk"]

    # End move original PK

    # Add fields to larger dict

    instruction_extra["fields"] = instruction_extra_fields

    for propertyprocess_instance in propertyprocess_dict:
        if (
            propertyprocess_instance["pk"]
            == instance["fields"]["propertyprocess"]
        ):
            if propertyprocess_instance["fields"]["sector"] == "lettings":
                instruction_extra_dict.append(instruction_extra)

    # End adding fields to larger dict

    # Create new UUID field

    instance["pk"] = str(uuid.uuid4())
    instruction_extra["pk"] = str(uuid.uuid4())

instruction_dict = instruction_model
instruction_lettings_extra_dict = instruction_extra_dict

with open(
    "/workspace/laurels-staff/common/data_dump/instruction.json", "w"
) as json_data:
    json.dump(instruction_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/instruction_letting_extra.json",
    "w",
) as json_data:
    json.dump(instruction_extra_dict, json_data)

# ----------------------------------------
# CREATE MASTER JSON
# ----------------------------------------

master_dict = []

for object in setup_dict:
    master_dict.append(object)

for object in hub_dict:
    master_dict.append(object)

for object in hub_targets_dict:
    master_dict.append(object)

for object in user_dict:
    master_dict.append(object)

for object in profile_dict:
    master_dict.append(object)

for object in totp_dict:
    master_dict.append(object)

for object in property_dict:
    master_dict.append(object)

for object in propertyprocess_dict:
    master_dict.append(object)

for object in property_history_dict:
    master_dict.append(object)

for object in super_dict:
    master_dict.append(object)

for object in valuation_dict:
    master_dict.append(object)

for object in instruction_dict:
    master_dict.append(object)

for object in instruction_lettings_extra_dict:
    master_dict.append(object)

with open(
    "/workspace/laurels-staff/common/data_dump/master.json", "w"
) as json_data:
    json.dump(master_dict, json_data)
