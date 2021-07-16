import humanize
import json
import uuid

from django.template.defaultfilters import slugify

from users.models import UserTargets, UserTargetsByYear

# ------------------------------------------------------------------------------
# COMMANDS
# ------------------------------------------------------------------------------

# python3 manage.py shell

# exec(open('common/data_change.py').read())


# python3 manage.py dumpdata home.hub > data/hub.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.targetshub > data/hubtargets.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata accounts.profile > data/profile.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata accounts.customuser > data/users.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata otp_totp.totpdevice > data/totp.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata accounts.targetsdynamic > data/usertargetsdynamic.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata accounts.targetsstatic > data/usertargetsstatic.json --settings=laurels_staff_portal.settings.production

# python3 manage.py dumpdata home.property > data/property.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.propertyprocess > data/property_process.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.valuation > data/valuation.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.instruction > data/instruction.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.offer > data/offer.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.deal > data/deal.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.exchangemove > data/exchangemove.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.salestatus > data/salesprogression.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.propertychain > data/propertychain.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.marketing > data/marketing.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.newbusiness > data/propertyfee.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.instructionchange > data/instructionchange.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.listingpricechange > data/listingpricechange.json --settings=laurels_staff_portal.settings.production
# python3 manage.py dumpdata home.dealchange > data/dealchange.json --settings=laurels_staff_portal.settings.production

# python3 manage.py flush

# python3 manage.py loaddata common/data_dump/master.json

# ------------------------------------------------------------------------------
# FUNCITONS
# ------------------------------------------------------------------------------

# unique = []
# non_unique = []

# if instance["fields"]["propertyprocess_link"] not in unique:
#     unique.append(instance["fields"]["propertyprocess_link"])
# elif instance["fields"]["propertyprocess_link"] not in non_unique:
#     non_unique.append(instance["fields"]["propertyprocess_link"])


# ------------------------------------------------------------------------------
# DICTIONARIES
# ------------------------------------------------------------------------------

setup_dict = None
super_dict = None
property_dict = None
propertyprocess_dict = None
property_history_dict = None
property_history_extra_dict = None
valuation_dict = None
instruction_dict = None
instruction_lettings_extra_dict = None
offerer_dict = None
offer_dict = None
deal_dict = None
exchange_dict = None
salesprogression_dict = None
salesprogressionsettings_dict = None
salesprogressionphase_dict = None
propertychain_dict = None
propertyfee_dict = None
marketing_dict = None
instruction_change_dict = None
instruction_change_new_dict = None
property_history_reduction_dict = None
progress_notes_dict = None
hub_dict = None
hub_targets_dict = None
user_dict = None
user_targets_dict = None
totp_dict = None
profile_dict = None
reduction_dict = None
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

    # Change Address Line 2

    if instance["fields"]["address_line_2"] == "":
        instance["fields"]["address_line_2"] = None

    # End change Address Line 2

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

# ----------------------------------------
# HUB TARGETS MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/hubtargets.json", "r"
) as json_data:
    hub_targets_model = json.load(json_data)

hub_targets = []

for instance in hub_targets_model:

    if instance["pk"] == 1:
        pass
    else:
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

        q1_2021_fields["reductions"] = instance["fields"][
            "q1_2021_reductions_hub"
        ]
        q2_2021_fields["reductions"] = instance["fields"][
            "q2_2021_reductions_hub"
        ]
        q3_2021_fields["reductions"] = instance["fields"][
            "q3_2021_reductions_hub"
        ]
        q4_2021_fields["reductions"] = instance["fields"][
            "q4_2021_reductions_hub"
        ]

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

    instance["old_target_link"] = instance["fields"]["target_link"]

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

# ----------------------------------------
# TARGETS MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/usertargetsdynamic.json",
    "r",
) as json_data:
    user_targets_model = json.load(json_data)

user_targets_dict = []

for instance in user_targets_model:

    q1 = {}
    q1_fields = {}

    q2 = {}
    q2_fields = {}

    q3 = {}
    q3_fields = {}

    q4 = {}
    q4_fields = {}

    year = {}
    year_fields = {}

    # Changing the model to new value

    q1["model"] = "users.usertargets"
    q2["model"] = "users.usertargets"
    q3["model"] = "users.usertargets"
    q4["model"] = "users.usertargets"
    year["model"] = "users.usertargetsbyyear"

    q1["pk"] = str(uuid.uuid4())
    q2["pk"] = str(uuid.uuid4())
    q3["pk"] = str(uuid.uuid4())
    q4["pk"] = str(uuid.uuid4())
    year["pk"] = str(uuid.uuid4())

    q1_fields["year"] = UserTargets.Y_2021
    q2_fields["year"] = UserTargets.Y_2021
    q3_fields["year"] = UserTargets.Y_2021
    q4_fields["year"] = UserTargets.Y_2021
    year_fields["year"] = UserTargetsByYear.Y_2021

    q1_fields["quarter"] = UserTargets.Q1
    q2_fields["quarter"] = UserTargets.Q2
    q3_fields["quarter"] = UserTargets.Q3
    q4_fields["quarter"] = UserTargets.Q4

    q1_fields["conveyancing"] = 6
    q2_fields["conveyancing"] = 6
    q3_fields["conveyancing"] = 6
    q4_fields["conveyancing"] = 6

    q1_fields["mortgages"] = 3
    q2_fields["mortgages"] = 3
    q3_fields["mortgages"] = 3
    q4_fields["mortgages"] = 3

    q1_fields["instructions"] = 18
    q2_fields["instructions"] = 18
    q3_fields["instructions"] = 18
    q4_fields["instructions"] = 18

    q1_fields["reductions"] = 12
    q2_fields["reductions"] = 12
    q3_fields["reductions"] = 12
    q4_fields["reductions"] = 12

    q1_fields["created_by"] = "Admin"
    q1_fields["created"] = "2000-01-13T13:13:13.000Z"
    q1_fields["updated_by"] = "Admin"
    q1_fields["updated"] = "2000-01-13T13:13:13.000Z"

    q2_fields["created_by"] = "Admin"
    q2_fields["created"] = "2000-01-13T13:13:13.000Z"
    q2_fields["updated_by"] = "Admin"
    q2_fields["updated"] = "2000-01-13T13:13:13.000Z"

    q3_fields["created_by"] = "Admin"
    q3_fields["created"] = "2000-01-13T13:13:13.000Z"
    q3_fields["updated_by"] = "Admin"
    q3_fields["updated"] = "2000-01-13T13:13:13.000Z"

    q4_fields["created_by"] = "Admin"
    q4_fields["created"] = "2000-01-13T13:13:13.000Z"
    q4_fields["updated_by"] = "Admin"
    q4_fields["updated"] = "2000-01-13T13:13:13.000Z"

    year_fields["created_by"] = "Admin"
    year_fields["created"] = "2000-01-13T13:13:13.000Z"
    year_fields["updated_by"] = "Admin"
    year_fields["updated"] = "2000-01-13T13:13:13.000Z"

    for profile_instance in profile_dict:
        if profile_instance["old_target_link"] == instance["pk"]:
            q1_fields["new_business"] = instance["fields"][
                "q1_2021_new_business"
            ]
            q2_fields["new_business"] = instance["fields"][
                "q2_2021_new_business"
            ]
            q3_fields["new_business"] = instance["fields"][
                "q3_2021_new_business"
            ]
            q4_fields["new_business"] = instance["fields"][
                "q4_2021_new_business"
            ]

            q1_fields["exchange_and_move"] = instance["fields"][
                "q1_2021_exchange_and_move"
            ]
            q2_fields["exchange_and_move"] = instance["fields"][
                "q2_2021_exchange_and_move"
            ]
            q3_fields["exchange_and_move"] = instance["fields"][
                "q3_2021_exchange_and_move"
            ]
            q4_fields["exchange_and_move"] = instance["fields"][
                "q4_2021_exchange_and_move"
            ]

            year_fields["targets_set"] = True

            q1_fields["profile_targets"] = profile_instance["pk"]
            q2_fields["profile_targets"] = profile_instance["pk"]
            q3_fields["profile_targets"] = profile_instance["pk"]
            q4_fields["profile_targets"] = profile_instance["pk"]

            q1_fields["user_targets"] = profile_instance["fields"]["user"]
            q2_fields["user_targets"] = profile_instance["fields"]["user"]
            q3_fields["user_targets"] = profile_instance["fields"]["user"]
            q4_fields["user_targets"] = profile_instance["fields"]["user"]

            year_fields["profile"] = profile_instance["pk"]
            year_fields["user"] = profile_instance["fields"]["user"]

            q1["fields"] = q1_fields
            q2["fields"] = q2_fields
            q3["fields"] = q3_fields
            q4["fields"] = q4_fields
            year["fields"] = year_fields

            if profile_instance["fields"]["employee_targets"] is True:
                user_targets_dict.append(q1)
                user_targets_dict.append(q2)
                user_targets_dict.append(q3)
                user_targets_dict.append(q4)
                user_targets_dict.append(year)

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
        instance["fields"]["macro_status"] = 1
        instance["fields"]["furthest_status"] = 1

    elif instance["fields"]["macro_status"] == "Instruction":
        instance["fields"]["macro_status"] = 2
        instance["fields"]["furthest_status"] = 2

    elif instance["fields"]["macro_status"] == "Viewing":
        instance["fields"]["macro_status"] = 3
        instance["fields"]["furthest_status"] = 3

    elif instance["fields"]["macro_status"] == "Deal":
        instance["fields"]["macro_status"] = 4
        instance["fields"]["furthest_status"] = 4

    elif instance["fields"]["macro_status"] == "Complete":
        instance["fields"]["macro_status"] = 5
        instance["fields"]["furthest_status"] = 5

    elif instance["fields"]["macro_status"] == "Withdrawn":
        instance["fields"]["macro_status"] = 0
        instance["fields"]["furthest_status"] = 3

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

    instance["fields"]["legacy_property"] = True
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

# ----------------------------------------
# PROPERTY HISTORY MODEL
# ----------------------------------------

history_temp_dict = []

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
        property_history_fields["description"] = (
            "This is a legacy property and property"
            " history is limited for this sale starts here."
        )
    else:
        property_history_fields["description"] = (
            "This is a legacy property and property"
            " history is limited for this letting starts here."
        )

    property_history_fields["created_by"] = "Admin"
    property_history_fields["created"] = "2000-01-13T13:13:13.000Z"
    property_history_fields["updated_by"] = "Admin"
    property_history_fields["updated"] = "2000-01-13T13:13:13.000Z"

    # End add new fields

    property_history["fields"] = property_history_fields

    history_temp_dict.append(property_history)

property_history_dict = history_temp_dict

# ----------------------------------------
# VALUATION MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/valuation.json",
    "r",
) as json_data:
    valuation_model = json.load(json_data)

history_extra = []

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

    # Loop user profile for valuer & delete old field

    for profile_instance in profile_dict:
        if profile_instance["old_pk"] == instance["fields"]["employee_valuer"]:
            instance["fields"]["valuer"] = profile_instance["pk"]

    del instance["fields"]["employee_valuer"]

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

    # Property history fields

    history = {}
    history_fields = {}

    # Add model

    history["model"] = "properties.propertyhistory"

    # End add model

    # Add new fields

    history_fields["propertyprocess"] = instance["fields"]["propertyprocess"]
    history_fields["created_by"] = "Admin"
    history_fields["updated_by"] = "Admin"
    history_fields["updated"] = "2000-01-13T13:13:13.000Z"

    history_fields["description"] = "The property has been valued."

    history_fields["created"] = instance["fields"]["date"]

    history_fields["type"] = "property_event"

    # Create new UUID field

    history["pk"] = str(uuid.uuid4())

    # End create new UUID field

    # End property history fields

    history["fields"] = history_fields

    history_extra.append(history)

valuation_dict = valuation_model

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
            instance["old_pp_pk"] = propertyprocess_instance["old_pk"]
            instruction_extra_fields[
                "propertyprocess"
            ] = propertyprocess_instance["pk"]
            instruction_extra["old_pp_pk"] = propertyprocess_instance["old_pk"]

    del instance["fields"]["propertyprocess_link"]

    # End loop

    # Changing the agreement_type to new values

    if instance["fields"]["agreement_type"] == "Sole":
        instance["fields"]["agreement_type"] = "sole"

    elif instance["fields"]["agreement_type"] == "Multi":
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

    elif instance["fields"]["lettings_service_level"] == "Fully Managed RI":
        instruction_extra_fields["lettings_service_level"] = "fully_managed"

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

    # Property history fields

    history = {}
    history_fields = {}

    # Add model

    history["model"] = "properties.propertyhistory"

    # End add model

    # Add new fields

    history_fields["propertyprocess"] = instance["fields"]["propertyprocess"]
    history_fields["created_by"] = "Admin"
    history_fields["updated_by"] = "Admin"
    history_fields["updated"] = "2000-01-13T13:13:13.000Z"

    history_fields["description"] = "The property has been instructed."

    history_fields["created"] = instance["fields"]["date"]

    history_fields["type"] = "property_event"

    # Create new UUID field

    history["pk"] = str(uuid.uuid4())

    # End create new UUID field

    # End property history fields

    history["fields"] = history_fields

    history_extra.append(history)

instruction_dict = instruction_model
instruction_lettings_extra_dict = instruction_extra_dict

# ----------------------------------------
# OFFER MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/offer.json",
    "r",
) as json_data:
    offer_model = json.load(json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/originals/deal.json",
    "r",
) as json_data:
    deal_model = json.load(json_data)

offerer_extra_dict = []

for instance in offer_model:

    offerer_extra = {}
    offerer_extra_fields = {}

    # Changing the model to new value

    instance["model"] = "properties.offer"
    offerer_extra["model"] = "properties.offererdetails"

    # End changing the model to new value

    # Loop property list for property process & delete old field

    for propertyprocess_instance in propertyprocess_dict:
        if (
            propertyprocess_instance["old_pk"]
            == instance["fields"]["propertyprocess_link"]
        ):
            offerer_extra_fields["propertyprocess"] = propertyprocess_instance[
                "pk"
            ]
            instance["old_pp_pk"] = propertyprocess_instance["old_pk"]
            instance["fields"]["propertyprocess"] = propertyprocess_instance[
                "pk"
            ]

    del instance["fields"]["propertyprocess_link"]

    # End loop

    # Change old field names

    instance["fields"]["date"] = instance["fields"]["offer_date"]

    del instance["fields"]["offer_date"]

    # Add new fields

    offerer_extra_fields["full_name"] = instance["fields"]["full_name"]
    del instance["fields"]["full_name"]

    offerer_extra_fields["created_by"] = "Admin"
    offerer_extra_fields["created"] = "2000-01-13T13:13:13.000Z"
    offerer_extra_fields["updated_by"] = "Admin"
    offerer_extra_fields["updated"] = "2000-01-13T13:13:13.000Z"

    instance["fields"]["created_by"] = "Admin"
    instance["fields"]["created"] = "2000-01-13T13:13:13.000Z"
    instance["fields"]["updated_by"] = "Admin"
    instance["fields"]["updated"] = "2000-01-13T13:13:13.000Z"

    # End add new fields

    # Add fields to larger dict

    offerer_extra["fields"] = offerer_extra_fields

    # End adding fields to larger dict

    # Move original PK

    instance["old_pk"] = instance["pk"]

    # End move original PK

    # Create new UUID field

    instance["pk"] = str(uuid.uuid4())

    offerer_extra["pk"] = str(uuid.uuid4())

    offerer_extra_dict.append(offerer_extra)

    # End new UUID field

    # Add UUID to link two new models

    instance["fields"]["offerer_details"] = offerer_extra["pk"]

    # End add UUID to link two new models

    # Change status' dependent on deals

    instance["fields"]["status"] = "negotiating"

    for deal_instance in deal_model:
        if (
            deal_instance["fields"]["propertyprocess_link"]
            == instance["old_pp_pk"]
        ):
            instance["fields"]["status"] = "rejected"

        if deal_instance["fields"]["offer_accepted"] == instance["old_pk"]:
            instance["fields"]["status"] = "accepted"

    for propertyprocess_instance in propertyprocess_dict:
        if (
            propertyprocess_instance["pk"]
            == instance["fields"]["propertyprocess"]
        ):
            if propertyprocess_instance["fields"]["macro_status"] == 0:
                instance["fields"]["status"] = "rejected"

offerer_dict = offerer_extra_dict

offer_dict = offer_model

# ----------------------------------------
# DEAL MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/deal.json",
    "r",
) as json_data:
    deal_model = json.load(json_data)

for instance in deal_model:

    # Changing the model to new value

    instance["model"] = "properties.deal"

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
            propertyprocess_instance["fields"]["furthest_status"] = 4

    del instance["fields"]["propertyprocess_link"]

    # End loop

    # Edit old fields

    instance["fields"]["date"] = instance["fields"]["deal_date"]
    del instance["fields"]["deal_date"]

    # Loop through offers

    for offer_instance in offer_dict:
        if offer_instance["old_pk"] == instance["fields"]["offer_accepted"]:
            instance["fields"]["offer_accepted"] = offer_instance["pk"]

    # End loop through offers

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

    # Property history fields

    history = {}
    history_fields = {}

    # Add model

    history["model"] = "properties.propertyhistory"

    # End add model

    # Add new fields

    history_fields["propertyprocess"] = instance["fields"]["propertyprocess"]
    history_fields["created_by"] = "Admin"
    history_fields["updated_by"] = "Admin"
    history_fields["updated"] = "2000-01-13T13:13:13.000Z"

    history_fields[
        "description"
    ] = "A deal has been processed for this property."

    history_fields["created"] = instance["fields"]["date"]

    history_fields["type"] = "property_event"

    # Create new UUID field

    history["pk"] = str(uuid.uuid4())

    # End create new UUID field

    # End property history fields

    history["fields"] = history_fields

    history_extra.append(history)

deal_dict = deal_model

# ----------------------------------------
# EXCHANGE MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/exchangemove.json",
    "r",
) as json_data:
    exchange_model = json.load(json_data)

exchange_dict = []

for instance in exchange_model:

    # Changing the model to new value

    instance["model"] = "properties.exchangemove"

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
            propertyprocess_instance["fields"]["furthest_status"] = 5

    del instance["fields"]["propertyprocess_link"]

    # End loop

    # Edit old fields

    instance["fields"]["exchange_date"] = instance["fields"][
        "exchange_move_in_date"
    ]
    instance["fields"]["completion_date"] = instance["fields"][
        "sales_completion_date"
    ]

    del instance["fields"]["exchange_move_in_date"]
    del instance["fields"]["sales_completion_date"]
    del instance["fields"]["lettings_renewal_date"]

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

    for propertyprocess_instance in propertyprocess_dict:
        if (
            propertyprocess_instance["pk"]
            == instance["fields"]["propertyprocess"]
        ):
            if propertyprocess_instance["fields"]["sector"] == "sales":
                exchange_dict.append(instance)

                # Property history fields

                history = {}
                history_fields = {}

                # Add model

                history["model"] = "properties.propertyhistory"

                # End add model

                # Add new fields

                history_fields["propertyprocess"] = instance["fields"][
                    "propertyprocess"
                ]
                history_fields["created_by"] = "Admin"
                history_fields["updated_by"] = "Admin"
                history_fields["updated"] = "2000-01-13T13:13:13.000Z"

                history_fields["description"] = "The property has exchanged."

                history_fields["created"] = instance["fields"]["exchange_date"]

                history_fields["type"] = "property_event"

                # Create new UUID field

                history["pk"] = str(uuid.uuid4())

                # End create new UUID field

                # End property history fields

                history["fields"] = history_fields

                history_extra.append(history)

# ----------------------------------------
# SALE PROGRESSION MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/salesprogression.json",
    "r",
) as json_data:
    saleprogression_model = json.load(json_data)

settings_extra = []
phase_extra = []
prog_notes_extra = []

for instance in saleprogression_model:

    settings = {}
    settings_fields = {}

    phase = {}
    phase_fields = {}

    prog_notes = {}
    prog_notes_fields = {}

    # Changing the model to new value

    instance["model"] = "properties.salesprogression"
    settings["model"] = "properties.salesprogressionsettings"
    phase["model"] = "properties.salesprogressionphase"
    prog_notes["model"] = "properties.progressionnotes"

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
            prog_notes_fields["propertyprocess"] = propertyprocess_instance[
                "pk"
            ]

    del instance["fields"]["propertyprocess_link"]

    # End loop

    # Move fields to new model

    settings_fields["show_mortgage"] = instance["fields"]["show_mortgage"]
    del instance["fields"]["show_mortgage"]

    settings_fields["show_survey"] = instance["fields"]["show_survey"]
    del instance["fields"]["show_survey"]

    prog_notes_fields["notes"] = instance["fields"]["sales_notes"]
    del instance["fields"]["sales_notes"]

    # End move fields to new model

    # Edit old fields

    instance["fields"]["buyers_aml_checks_and_sales_memo"] = instance[
        "fields"
    ]["laurels_aml_checks_complete"]
    del instance["fields"]["laurels_aml_checks_complete"]

    instance["fields"]["buyers_aml_checks_and_sales_memo_date"] = instance[
        "fields"
    ]["laurels_aml_checks_complete_date"]
    del instance["fields"]["laurels_aml_checks_complete_date"]

    instance["fields"]["buyers_initial_solicitors_paperwork"] = instance[
        "fields"
    ]["buyers_initial_solicitors_paperwork_complete"]
    del instance["fields"]["buyers_initial_solicitors_paperwork_complete"]

    instance["fields"]["buyers_initial_solicitors_paperwork_date"] = instance[
        "fields"
    ]["buyers_initial_solicitors_paperwork_complete_date"]
    del instance["fields"]["buyers_initial_solicitors_paperwork_complete_date"]

    instance["fields"]["sellers_inital_solicitors_paperwork"] = instance[
        "fields"
    ]["sellers_inital_solicitors_paperwork_complete"]
    del instance["fields"]["sellers_inital_solicitors_paperwork_complete"]

    instance["fields"]["sellers_inital_solicitors_paperwork_date"] = instance[
        "fields"
    ]["sellers_inital_solicitors_paperwork_complete_date"]
    del instance["fields"]["sellers_inital_solicitors_paperwork_complete_date"]

    instance["fields"]["mortgage_offer_with_solicitors"] = instance["fields"][
        "mortgage_survey_completed"
    ]
    del instance["fields"]["mortgage_survey_completed"]

    instance["fields"]["mortgage_offer_with_solicitors_date"] = instance[
        "fields"
    ]["mortgage_survey_completed_date"]
    del instance["fields"]["mortgage_survey_completed_date"]

    # del old fields

    del instance["fields"]["fallen_through"]
    del instance["fields"]["fallen_through_date"]

    # end del old fields

    # Create phase counts

    phase_fields["phase_1"] = False
    phase_fields["phase_2"] = False
    phase_fields["phase_3"] = False
    phase_fields["phase_4"] = False

    if (
        instance["fields"]["buyers_aml_checks_and_sales_memo"]
        and instance["fields"]["buyers_initial_solicitors_paperwork"]
        and instance["fields"]["sellers_inital_solicitors_paperwork"]
        and instance["fields"]["draft_contracts_recieved_by_buyers_solicitors"]
        and instance["fields"]["searches_paid_for"]
        and instance["fields"]["searches_ordered"]
    ):
        phase_fields["phase_1"] = True
        phase_fields["overall_phase"] = 1

    if settings_fields["show_mortgage"] is True:
        if (
            instance["fields"]["mortgage_application_submitted"]
            and instance["fields"]["mortgage_survey_arranged"]
            and instance["fields"]["mortgage_offer_with_solicitors"]
            and instance["fields"]["all_search_results_recieved"]
        ):
            phase_fields["phase_2"] = True
            if phase_fields["phase_1"] is True:
                phase_fields["overall_phase"] = 2
    else:
        if instance["fields"]["all_search_results_recieved"]:
            phase_fields["phase_2"] = True
            if phase_fields["phase_1"] is True:
                phase_fields["overall_phase"] = 2

    if settings_fields["show_survey"] is True:
        if (
            instance["fields"]["structural_survey_booked"]
            and instance["fields"]["structural_survey_completed"]
            and instance["fields"]["enquiries_raised"]
            and instance["fields"]["enquiries_answered"]
        ):
            phase_fields["phase_3"] = True
            if (
                phase_fields["phase_1"] is True
                and phase_fields["phase_2"] is True
            ):
                phase_fields["overall_phase"] = 3
    else:
        if (
            instance["fields"]["enquiries_raised"]
            and instance["fields"]["enquiries_answered"]
        ):
            phase_fields["phase_3"] = True
            if (
                phase_fields["phase_1"] is True
                and phase_fields["phase_2"] is True
            ):
                phase_fields["overall_phase"] = 3

    if (
        instance["fields"]["additional_enquiries_raised"]
        and instance["fields"]["all_enquiries_answered"]
        and instance["fields"]["final_contracts_sent_out"]
        and instance["fields"]["buyers_final_contracts_signed"]
        and instance["fields"]["sellers_final_contracts_signed"]
        and instance["fields"]["buyers_deposit_sent"]
        and instance["fields"]["buyers_deposit_recieved"]
        and instance["fields"]["completion_date_agreed"]
    ):
        phase_fields["phase_4"] = True
        if (
            phase_fields["phase_1"] is True
            and phase_fields["phase_2"] is True
            and phase_fields["phase_3"] is True
        ):
            phase_fields["overall_phase"] = 4

    # End create phase counts

    # Add new fields

    instance["fields"]["created_by"] = "Admin"
    instance["fields"]["created"] = "2000-01-13T13:13:13.000Z"
    instance["fields"]["updated_by"] = "Admin"
    instance["fields"]["updated"] = "2000-01-13T13:13:13.000Z"

    settings_fields["created_by"] = "Admin"
    settings_fields["created"] = "2000-01-13T13:13:13.000Z"
    settings_fields["updated_by"] = "Admin"
    settings_fields["updated"] = "2000-01-13T13:13:13.000Z"

    phase_fields["created_by"] = "Admin"
    phase_fields["created"] = "2000-01-13T13:13:13.000Z"
    phase_fields["updated_by"] = "Admin"
    phase_fields["updated"] = "2000-01-13T13:13:13.000Z"

    prog_notes_fields["created_by"] = "Admin"
    prog_notes_fields["created"] = "2000-01-13T13:13:13.000Z"
    prog_notes_fields["updated_by"] = "Admin"
    prog_notes_fields["updated"] = "2000-01-13T13:13:13.000Z"

    # End add new fields

    # Move original PK

    instance["old_pk"] = instance["pk"]

    # End move original PK

    # Create new UUID field

    instance["pk"] = str(uuid.uuid4())
    settings["pk"] = str(uuid.uuid4())
    phase["pk"] = str(uuid.uuid4())

    # New model extra fields

    settings_fields["sales_progression"] = instance["pk"]
    phase_fields["sales_progression"] = instance["pk"]
    phase["old_sp_pk"] = instance["old_pk"]

    settings["fields"] = settings_fields
    phase["fields"] = phase_fields
    prog_notes["fields"] = prog_notes_fields

    settings_extra.append(settings)
    phase_extra.append(phase)
    prog_notes_extra.append(prog_notes)

    # End new model extra fields

salesprogression_dict = saleprogression_model
salesprogressionsettings_dict = settings_extra
salesprogressionphase_dict = phase_extra
progress_notes_dict = prog_notes_extra

# ----------------------------------------
# PROPERTY CHAIN MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/propertychain.json",
    "r",
) as json_data:
    propertychain_model = json.load(json_data)

for instance in propertychain_model:

    # Changing the model to new value

    instance["model"] = "properties.propertychain"

    # End changing the model to new value

    # Loop sales progression for link & delete old field

    for salesprogression_instance in salesprogression_dict:
        if (
            salesprogression_instance["old_pk"]
            == instance["fields"]["sale_status_link"]
        ):
            instance["fields"]["propertyprocess"] = salesprogression_instance[
                "fields"
            ]["propertyprocess"]

    del instance["fields"]["sale_status_link"]

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

propertychain_dict = propertychain_model

# ----------------------------------------
# MARKETING MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/marketing.json",
    "r",
) as json_data:
    marketing_model = json.load(json_data)

for instance in marketing_model:

    # Changing the model to new value

    instance["model"] = "properties.marketing"

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

    # Changing the old values to new values

    if instance["fields"]["hear_about_laurels"] == "Previous Client":
        instance["fields"]["hear_about_laurels"] = "previous_client"
    elif instance["fields"]["hear_about_laurels"] == "Applicant":
        instance["fields"]["hear_about_laurels"] = "applicant"
    elif instance["fields"]["hear_about_laurels"] == "Social Media Posts":
        instance["fields"]["hear_about_laurels"] = "social_media"
    elif instance["fields"]["hear_about_laurels"] == "Recommendation":
        instance["fields"]["hear_about_laurels"] = "recommendation"
    elif (
        instance["fields"]["hear_about_laurels"]
        == "Laurels Team Member/Friends or Family of Laurels"
    ):
        instance["fields"][
            "hear_about_laurels"
        ] = "laurels_team_member_friends_or_family_of_laurels"
    elif instance["fields"]["hear_about_laurels"] == "Sold/Let Flyer":
        instance["fields"]["hear_about_laurels"] = "sold_let_flyer"
    elif instance["fields"]["hear_about_laurels"] == "Tout Letter":
        instance["fields"]["hear_about_laurels"] = "tout_letter"
    elif instance["fields"]["hear_about_laurels"] == "Specific Letter":
        instance["fields"]["hear_about_laurels"] = "specific_letter"
    elif instance["fields"]["hear_about_laurels"] == "Brochure Drop":
        instance["fields"]["hear_about_laurels"] = "brochure"
    elif instance["fields"]["hear_about_laurels"] == "Business Card Drop":
        instance["fields"]["hear_about_laurels"] = "business_card_drop"
    elif instance["fields"]["hear_about_laurels"] == "Combined Touting":
        instance["fields"]["hear_about_laurels"] = "combined_touting"
    elif instance["fields"]["hear_about_laurels"] == "Google Search":
        instance["fields"]["hear_about_laurels"] = "google_search"
    elif instance["fields"]["hear_about_laurels"] == "Marketing Boards":
        instance["fields"]["hear_about_laurels"] = "marketing_boards"
    elif instance["fields"]["hear_about_laurels"] == "Local Presence":
        instance["fields"]["hear_about_laurels"] = "local_presence"
    elif instance["fields"]["hear_about_laurels"] == "Sold on Road":
        instance["fields"]["hear_about_laurels"] = "sold_on_road"

    if instance["fields"]["applicant_intro"] == "Rightmove":
        instance["fields"]["applicant_intro"] = "rightmove"
    elif instance["fields"]["applicant_intro"] == "Zoopla":
        instance["fields"]["applicant_intro"] = "zoopla"
    elif instance["fields"]["applicant_intro"] == "Social Media":
        instance["fields"]["applicant_intro"] = "social_media"
    elif instance["fields"]["applicant_intro"] == "Laurels Website Search":
        instance["fields"]["applicant_intro"] = "laurels_website_search"
    elif instance["fields"]["applicant_intro"] == "Laurels Team Recommended":
        instance["fields"]["applicant_intro"] = "laurels_team_recommended"
    elif instance["fields"]["applicant_intro"] == "Marketing Boards":
        instance["fields"]["applicant_intro"] = "marketing_boards"
    elif instance["fields"]["applicant_intro"] == "Public Word of Mouth":
        instance["fields"]["applicant_intro"] = "public_word_of_mouth"

    if instance["fields"]["contact_laurels"] == "Laurels Pro-actively Asked":
        instance["fields"]["contact_laurels"] = "laurels_pro-actively_asked"
    elif instance["fields"]["contact_laurels"] == "Social Media Message":
        instance["fields"]["contact_laurels"] = "social_media_message"
    elif instance["fields"]["contact_laurels"] == "Phone Call To Office":
        instance["fields"]["contact_laurels"] = "phone_call_to_office"
    elif instance["fields"]["contact_laurels"] == "Website Message":
        instance["fields"]["contact_laurels"] = "website_message"
    elif instance["fields"]["contact_laurels"] == "Direct Email":
        instance["fields"]["contact_laurels"] = "direct_email"

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

marketing_dict = marketing_model

# ----------------------------------------
# PROPERTY FEE MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/propertyfee.json",
    "r",
) as json_data:
    property_fee_model = json.load(json_data)

for instance in property_fee_model:

    # Changing the model to new value

    instance["model"] = "properties.propertyfees"

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

    # Edit old fields

    instance["fields"]["price"] = instance["fields"]["final_price"]
    del instance["fields"]["final_price"]

    instance["fields"]["fee"] = instance["fields"]["final_fee"]
    del instance["fields"]["final_fee"]

    instance["fields"]["new_business"] = instance["fields"]["calculated_value"]
    del instance["fields"]["calculated_value"]

    instance["fields"]["active"] = instance["fields"]["deal_time"]
    del instance["fields"]["deal_time"]

    instance["fields"]["date"] = instance["fields"]["deal_date"]
    del instance["fields"]["deal_date"]

    del instance["fields"]["sector"]

    # End edit old fields

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

propertyfee_dict = property_fee_model

# ----------------------------------------
# INSTRUCTION CHANGE MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/instructionchange.json",
    "r",
) as json_data:
    instruction_change_model = json.load(json_data)

withdrawn_but_active = []
inst_change_dict = []

print("Fee Change Properties:")
for instance in instruction_change_model:

    history_withdrawn = {}
    history_withdrawn_fields = {}

    history_agreement_type_change = {}
    history_agreement_type_change_fields = {}

    history_fee_agreed_change = {}
    history_fee_agreed_change_fields = {}

    history_length_of_contract_change = {}
    history_length_of_contract_change_fields = {}

    history_lettings_service_level_change = {}
    history_lettings_service_level_change_fields = {}

    instruction_change = {}
    instruction_change_fields = {}

    # Changing the model to new value

    history_withdrawn["model"] = "properties.propertyhistory"
    history_agreement_type_change["model"] = "properties.propertyhistory"
    history_fee_agreed_change["model"] = "properties.propertyhistory"
    history_length_of_contract_change["model"] = "properties.propertyhistory"
    history_lettings_service_level_change[
        "model"
    ] = "properties.propertyhistory"
    instruction_change["model"] = "properties.instructionchange"

    # End changing the model to new value

    # Loop property list for property process & delete old field

    for propertyprocess_instance in propertyprocess_dict:
        if (
            propertyprocess_instance["old_pk"]
            == instance["fields"]["propertyprocess_link"]
        ):
            instance["new_pp_pk"] = propertyprocess_instance["pk"]
            history_withdrawn_fields[
                "propertyprocess"
            ] = propertyprocess_instance["pk"]
            history_agreement_type_change_fields[
                "propertyprocess"
            ] = propertyprocess_instance["pk"]
            history_fee_agreed_change_fields[
                "propertyprocess"
            ] = propertyprocess_instance["pk"]
            history_length_of_contract_change_fields[
                "propertyprocess"
            ] = propertyprocess_instance["pk"]
            history_lettings_service_level_change_fields[
                "propertyprocess"
            ] = propertyprocess_instance["pk"]
            instruction_change_fields[
                "propertyprocess"
            ] = propertyprocess_instance["pk"]

            history_withdrawn["old_pp_pk"] = instance["fields"][
                "propertyprocess_link"
            ]
            history_agreement_type_change["old_pp_pk"] = instance["fields"][
                "propertyprocess_link"
            ]
            history_fee_agreed_change["old_pp_pk"] = instance["fields"][
                "propertyprocess_link"
            ]
            history_length_of_contract_change["old_pp_pk"] = instance[
                "fields"
            ]["propertyprocess_link"]
            history_lettings_service_level_change["old_pp_pk"] = instance[
                "fields"
            ]["propertyprocess_link"]
            instruction_change["old_pp_pk"] = instance["fields"][
                "propertyprocess_link"
            ]

    # End loop

    # Add new fields

    history_withdrawn_fields["created_by"] = "Admin"
    history_withdrawn_fields["updated_by"] = "Admin"
    history_withdrawn_fields["updated"] = "2000-01-13T13:13:13.000Z"

    history_agreement_type_change_fields["created_by"] = "Admin"
    history_agreement_type_change_fields["updated_by"] = "Admin"
    history_agreement_type_change_fields[
        "updated"
    ] = "2000-01-13T13:13:13.000Z"

    history_fee_agreed_change_fields["created_by"] = "Admin"
    history_fee_agreed_change_fields["updated_by"] = "Admin"
    history_fee_agreed_change_fields["updated"] = "2000-01-13T13:13:13.000Z"

    history_length_of_contract_change_fields["created_by"] = "Admin"
    history_length_of_contract_change_fields["updated_by"] = "Admin"
    history_length_of_contract_change_fields[
        "updated"
    ] = "2000-01-13T13:13:13.000Z"

    history_lettings_service_level_change_fields["created_by"] = "Admin"
    history_lettings_service_level_change_fields["updated_by"] = "Admin"
    history_lettings_service_level_change_fields[
        "updated"
    ] = "2000-01-13T13:13:13.000Z"

    instruction_change_fields["created_by"] = "Admin"
    instruction_change_fields["updated_by"] = "Admin"
    instruction_change_fields["created"] = instance["fields"][
        "instruction_change_date"
    ]
    instruction_change_fields["updated"] = "2000-01-13T13:13:13.000Z"

    # End add new fields

    # Property history fields

    history_withdrawn_fields["type"] = "property_event"
    history_agreement_type_change_fields["type"] = "property_event"
    history_fee_agreed_change_fields["type"] = "property_event"
    history_length_of_contract_change_fields["type"] = "property_event"
    history_lettings_service_level_change_fields["type"] = "property_event"

    # End property history fields

    instruction_change_fields["agreement_type_bool"] = False
    instruction_change_fields["fee_agreed_bool"] = False
    instruction_change_fields["length_of_contract_bool"] = False

    if instance["fields"]["withdrawn"] is True:

        for property_process_instance in propertyprocess_dict:
            if (
                instance["fields"]["propertyprocess_link"]
                == property_process_instance["old_pk"]
            ):
                if property_process_instance["fields"]["macro_status"] == 0:
                    for property_fee_instance in propertyfee_dict:
                        if (
                            property_fee_instance["fields"]["propertyprocess"]
                            == property_process_instance["pk"]
                        ):
                            if (
                                property_fee_instance["fields"]["active"]
                                is True
                            ):
                                if (
                                    property_process_instance["pk"]
                                    not in withdrawn_but_active
                                ):
                                    withdrawn_but_active.append(
                                        property_process_instance["pk"]
                                    )
        # Property history fields

        history_withdrawn_fields[
            "description"
        ] = "This property has been withdrawn from the market."

        history_withdrawn_fields["notes"] = instance["fields"][
            "withdrawn_reason"
        ]
        history_withdrawn_fields["created"] = instance["fields"][
            "instruction_change_date"
        ]

        # Create new UUID field

        history_withdrawn["pk"] = str(uuid.uuid4())

        # End create new UUID field

        # End property history fields

        history_withdrawn["fields"] = history_withdrawn_fields

        history_extra.append(history_withdrawn)

    if instance["fields"]["agreement_type_change"] is not None:

        instruction_change_fields["agreement_type_bool"] = True

        if instance["fields"]["agreement_type_change"] == "Multi To Sole":
            instruction_change_fields["agreement_type"] = "sole"
        else:
            instruction_change_fields["agreement_type"] = "multi"

        # Property history fields

        history_agreement_type_change_fields[
            "description"
        ] = "There has been an instruction agreement type change."

        history_agreement_type_change_fields["notes"] = instance["fields"][
            "agreement_type_change"
        ]
        history_agreement_type_change_fields["created"] = instance["fields"][
            "instruction_change_date"
        ]

        # Create new UUID field

        history_agreement_type_change["pk"] = str(uuid.uuid4())

        # End create new UUID field

        # End property history fields

        history_agreement_type_change[
            "fields"
        ] = history_agreement_type_change_fields

        history_extra.append(history_agreement_type_change)

    if instance["fields"]["fee_agreed_change"] is not None:

        instruction_change_fields["fee_agreed_bool"] = True

        instruction_change_fields["fee_agreed"] = instance["fields"][
            "fee_agreed_change"
        ]

        # Property history fields

        history_fee_agreed_change_fields[
            "description"
        ] = "There has been an instruction fee change."

        new_fee = instance["fields"]["fee_agreed_change"]

        new_property_fee = {}
        new_property_fee_fields = {}

        for instruction_instance in instruction_dict:
            if (
                instruction_instance["old_pp_pk"]
                == instance["fields"]["propertyprocess_link"]
            ):
                old_fee = instruction_instance["fields"]["fee_agreed"]

                new_property_fee["model"] = "properties.propertyfees"

                new_property_fee_fields[
                    "propertyprocess"
                ] = history_fee_agreed_change_fields["propertyprocess"]

                new_property_fee_fields["price"] = instruction_instance[
                    "fields"
                ]["listing_price"]

                new_property_fee_fields["fee"] = new_fee

                new_property_fee_fields["date"] = instance["fields"][
                    "instruction_change_date"
                ]

                new_property_fee_fields["created_by"] = "Admin"
                new_property_fee_fields["created"] = instance["fields"][
                    "instruction_change_date"
                ]
                new_property_fee_fields["updated_by"] = "Admin"
                new_property_fee_fields["updated"] = "2000-01-13T13:13:13.000Z"

                new_property_fee["pk"] = str(uuid.uuid4())

                new_property_fee["fields"] = new_property_fee_fields

                propertyfee_dict.append(new_property_fee)

        for property_process_instance in propertyprocess_dict:
            if (
                instance["fields"]["propertyprocess_link"]
                == property_process_instance["old_pk"]
            ):
                if property_process_instance["fields"]["macro_status"] == 0:
                    print("Withdrawn -", property_process_instance["old_pk"])
                elif property_process_instance["fields"]["macro_status"] == 1:
                    print(
                        "*****ALERT*****  Awaiting Valuation -",
                        property_process_instance["old_pk"],
                    )
                elif property_process_instance["fields"]["macro_status"] == 2:
                    print(
                        "*****ALERT*****  Valuation Complete -",
                        property_process_instance["old_pk"],
                    )
                elif property_process_instance["fields"]["macro_status"] == 3:
                    print(
                        "*****ALERT***** Instructed - On The Market -",
                        property_process_instance["old_pk"],
                    )
                elif property_process_instance["fields"]["macro_status"] == 4:
                    print("Deal -", property_process_instance["old_pk"])
                elif property_process_instance["fields"]["macro_status"] == 5:
                    print("Complete -", property_process_instance["old_pk"])

        note = f"The fee has been changed from {old_fee}% to {new_fee}%"

        history_fee_agreed_change_fields["notes"] = note
        history_fee_agreed_change_fields["created"] = instance["fields"][
            "instruction_change_date"
        ]
        instruction_instance["fields"]["updated"] = instance["fields"][
            "instruction_change_date"
        ]

        # Create new UUID field

        history_fee_agreed_change["pk"] = str(uuid.uuid4())

        # End create new UUID field

        # End property history fields

        history_fee_agreed_change["fields"] = history_fee_agreed_change_fields

        history_extra.append(history_fee_agreed_change)

    if instance["fields"]["length_of_contract_change"] is not None:

        print("*****ALERT***** There is a length change *****ALERT*****")

        instruction_change_fields["length_of_contract_bool"] = True

        instruction_change_fields["length_of_contract"] = instance["fields"][
            "length_of_contract_change"
        ]

    if instance["fields"]["lettings_service_level_change"] is not None:

        # Property history fields

        history_lettings_service_level_change_fields[
            "description"
        ] = "There has been an instruction service level change."

        new_fee = instance["fields"]["fee_agreed_change"]

        for instruction_instance in instruction_lettings_extra_dict:
            if (
                instruction_instance["old_pp_pk"]
                == instance["fields"]["propertyprocess_link"]
            ):
                old_service_level = instruction_instance["fields"][
                    "lettings_service_level"
                ]

                if (
                    instance["fields"]["lettings_service_level_change"]
                    == "Intro Only"
                ):
                    new_service_level = "'Intro Only'"
                    new_service_level_programatic = "intro_only"
                    managed = False

                elif (
                    instance["fields"]["lettings_service_level_change"]
                    == "Rent Collect"
                ):
                    new_service_level = "'Rent Collect'"
                    new_service_level_programatic = "rent_collect"
                    managed = True

                elif (
                    instance["fields"]["lettings_service_level_change"]
                    == "Fully Managed"
                ):
                    new_service_level = "'Fully Managed'"
                    new_service_level_programatic = "fully_managed"
                    managed = True

                elif (
                    instance["fields"]["lettings_service_level_change"]
                    == "Fully Managed RI"
                ):
                    new_service_level = "'Fully Managed'"
                    new_service_level_programatic = "fully_managed"
                    managed = True

                if old_service_level == "intro_only":
                    old_service_level = "'Intro Only'"

                elif old_service_level == "rent_collect":
                    old_service_level = "'Rent Collect'"

                elif old_service_level == "fully_managed":
                    old_service_level = "'Fully Managed'"

                elif old_service_level == "fully_managed_ri":
                    old_service_level = "'Fully Managed'"

                instruction_instance["fields"][
                    "lettings_service_level"
                ] = new_service_level_programatic
                instruction_instance["fields"]["managed_property"] = managed
                instruction_instance["fields"]["updated"] = instance["fields"][
                    "instruction_change_date"
                ]

        note = (
            f"The service level has been changed from {old_service_level}"
            f" to {new_service_level}"
        )

        history_lettings_service_level_change_fields["notes"] = note
        history_lettings_service_level_change_fields["created"] = instance[
            "fields"
        ]["instruction_change_date"]

        # Create new UUID field

        history_lettings_service_level_change["pk"] = str(uuid.uuid4())

        # End create new UUID field

        # End property history fields

        history_lettings_service_level_change[
            "fields"
        ] = history_lettings_service_level_change_fields

        history_extra.append(history_lettings_service_level_change)

    # Create new UUID field

    instruction_change["pk"] = str(uuid.uuid4())

    instruction_change["fields"] = instruction_change_fields

    if (
        instruction_change_fields["agreement_type_bool"] is True
        or instruction_change_fields["fee_agreed_bool"] is True
        or instruction_change_fields["length_of_contract_bool"] is True
    ):
        inst_change_dict.append(instruction_change)

    # End create new UUID field

print("")
print("Withdrawn But Active, Properties:")
for instance in withdrawn_but_active:
    print(instance)

property_history_extra_dict = history_extra
instruction_change_dict = instruction_change_model
instruction_change_new_dict = inst_change_dict

# ----------------------------------------
# REDUCTION MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/listingpricechange.json",
    "r",
) as json_data:
    reduction_model = json.load(json_data)

property_history_reduction_dict = []

reduction_dict = []

for instance in reduction_model:

    if instance["fields"]["date"] is None:
        pass
    else:

        reduction = {}
        reduction_fields = {}

        # Changing the model to new value

        instance["model"] = "properties.propertyhistory"

        reduction["model"] = "properties.reduction"

        # End changing the model to new value

        # Loop property list for property process & delete old field

        for instruction_change_instance in instruction_change_dict:
            if (
                instruction_change_instance["pk"]
                == instance["fields"]["instruction_change"]
            ):
                instance["fields"][
                    "propertyprocess"
                ] = instruction_change_instance["new_pp_pk"]

        del instance["fields"]["instruction_change"]

        reduction_fields["propertyprocess"] = instance[
            "fields"
        ]["propertyprocess"]

        # End loop

        # Add property history fields

        pp_reduction_history_dict = []

        for prop_history_reduction_instance in property_history_reduction_dict:
            if (
                instance["fields"]["propertyprocess"]
                == prop_history_reduction_instance["fields"]["propertyprocess"]
            ):
                pp_reduction_history_dict.append(
                    prop_history_reduction_instance
                )

        instance["fields"]["type"] = "property_event"
        instance["fields"]["description"] = "There has been a price reduction."

        new_price = instance["fields"]["price_change"]

        reduction_fields["price_change"] = instance["fields"]["price_change"]

        if len(pp_reduction_history_dict) == 0:
            notes = (
                "The price has been reduced"
                f" from listing price to £{humanize.intcomma(new_price)}"
            )

        else:
            last = pp_reduction_history_dict[-1]
            old_price = last["old_price"]
            notes = (
                "The price has been reduced from "
                f"£{humanize.intcomma(old_price)}"
                f" to £{humanize.intcomma(new_price)}"
            )

        instance["fields"]["notes"] = notes

        instance["old_price"] = instance["fields"]["price_change"]
        del instance["fields"]["price_change"]

        # End add property history fields

        # Add new fields

        reduction_fields["created_by"] = "Admin"
        reduction_fields["created"] = instance["fields"]["date"]
        reduction_fields["date"] = instance["fields"]["date"]
        reduction_fields["updated_by"] = "Admin"
        reduction_fields["updated"] = "2000-01-13T13:13:13.000Z"

        instance["fields"]["created_by"] = "Admin"
        instance["fields"]["created"] = instance["fields"]["date"]
        del instance["fields"]["date"]
        instance["fields"]["updated_by"] = "Admin"
        instance["fields"]["updated"] = "2000-01-13T13:13:13.000Z"

        # End add new fields

        # Move original PK

        instance["old_pk"] = instance["pk"]

        # End move original PK

        # Create new UUID field

        instance["pk"] = str(uuid.uuid4())
        reduction["pk"] = str(uuid.uuid4())

        reduction["fields"] = reduction_fields

        reduction_dict.append(reduction)

        # Create a new property fee for reduction only if
        # they aren't passed instruction

        previous_prop_fee = []

        for prop_fee_instance in propertyfee_dict:
            if (
                prop_fee_instance["fields"]["propertyprocess"]
                == instance["fields"]["propertyprocess"]
            ):
                previous_prop_fee.append(prop_fee_instance)

        last = previous_prop_fee[-1]

        new_property_fee = {}
        new_property_fee_fields = {}

        for propertyprocess_instance in propertyprocess_dict:
            if (
                propertyprocess_instance["pk"]
                == instance["fields"]["propertyprocess"]
            ):
                if (
                    propertyprocess_instance["fields"]["macro_status"] > 0
                    and propertyprocess_instance["fields"]["macro_status"] < 4
                ):
                    new_property_fee["model"] = "properties.propertyfees"

                    new_property_fee_fields[
                        "propertyprocess"
                    ] = propertyprocess_instance["pk"]

                    new_property_fee_fields["price"] = new_price

                    new_property_fee_fields["fee"] = last["fields"]["fee"]

                    new_property_fee_fields["date"] = instance["fields"][
                        "created"
                    ]

                    new_property_fee_fields["created_by"] = "Admin"
                    new_property_fee_fields["created"] = instance["fields"][
                        "created"
                    ]
                    new_property_fee_fields["updated_by"] = "Admin"
                    new_property_fee_fields[
                        "updated"
                    ] = "2000-01-13T13:13:13.000Z"

                    new_property_fee["pk"] = str(uuid.uuid4())

                    new_property_fee["fields"] = new_property_fee_fields

                    propertyfee_dict.append(new_property_fee)

        property_history_reduction_dict.append(instance)

# ----------------------------------------
# DEAL CHANGE MODEL
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/dealchange.json",
    "r",
) as json_data:
    deal_change_model = json.load(json_data)

for instance in deal_change_model:

    if instance["fields"]["deal_change_date"] is not None:
        history_price_agreed_change = {}
        history_price_agreed_change_fields = {}

        history_fee_agreed_change = {}
        history_fee_agreed_change_fields = {}

        # Changing the model to new value

        history_price_agreed_change["model"] = "properties.propertyhistory"
        history_fee_agreed_change["model"] = "properties.propertyhistory"

        # End changing the model to new value

        # Loop property list for property process & delete old field

        for propertyprocess_instance in propertyprocess_dict:
            if (
                propertyprocess_instance["old_pk"]
                == instance["fields"]["propertyprocess_link"]
            ):
                instance["new_pp_pk"] = propertyprocess_instance["pk"]
                history_price_agreed_change_fields[
                    "propertyprocess"
                ] = propertyprocess_instance["pk"]

                history_fee_agreed_change_fields[
                    "propertyprocess"
                ] = propertyprocess_instance["pk"]

                history_price_agreed_change["old_pp_pk"] = instance["fields"][
                    "propertyprocess_link"
                ]

                history_fee_agreed_change["old_pp_pk"] = instance["fields"][
                    "propertyprocess_link"
                ]

        # End loop

        # Add new fields

        history_fee_agreed_change_fields["created_by"] = "Admin"
        history_fee_agreed_change_fields["updated_by"] = "Admin"
        history_fee_agreed_change_fields[
            "updated"
        ] = "2000-01-13T13:13:13.000Z"

        history_price_agreed_change_fields["created_by"] = "Admin"
        history_price_agreed_change_fields["updated_by"] = "Admin"
        history_price_agreed_change_fields[
            "updated"
        ] = "2000-01-13T13:13:13.000Z"

        if instance["fields"]["deal_price_agreed_change"]:
            # Property history fields

            history_price_agreed_change_fields[
                "description"
            ] = "There has been an deal price agreed change."

            new_price = instance["fields"]["deal_price_agreed_change"]

            for prop_fee_instance in propertyfee_dict:
                if (
                    prop_fee_instance["fields"]["propertyprocess"]
                    == instance["new_pp_pk"]
                ):
                    previous_prop_fee.append(prop_fee_instance)

            last = previous_prop_fee[-1]

            for offer_instance in offer_dict:
                if (
                    offer_instance["fields"]["propertyprocess"]
                    == instance["new_pp_pk"]
                ):
                    if offer_instance["fields"]["status"] == "accepted":

                        old_price = offer_instance["fields"]["offer"]

            note = f"The agreed price has changed from £{humanize.intcomma(old_price)} to £{humanize.intcomma(new_price)}"

            history_price_agreed_change_fields["notes"] = note
            history_price_agreed_change_fields["created"] = instance["fields"][
                "deal_change_date"
            ]
            history_price_agreed_change_fields["type"] = "property_event"

            # Create new UUID field

            history_price_agreed_change["pk"] = str(uuid.uuid4())

            # End create new UUID field

            # End property history fields

            history_price_agreed_change[
                "fields"
            ] = history_price_agreed_change_fields

            property_history_extra_dict.append(history_price_agreed_change)

        if instance["fields"]["deal_fee_agreed_change"]:
            # Property history fields

            history_fee_agreed_change_fields[
                "description"
            ] = "There has been a fee change for the deal."

            new_fee = instance["fields"]["deal_fee_agreed_change"]

            previous_prop_fee = []

            for prop_fee_instance in propertyfee_dict:
                if (
                    prop_fee_instance["fields"]["propertyprocess"]
                    == instance["new_pp_pk"]
                ):
                    previous_prop_fee.append(prop_fee_instance)

            last = previous_prop_fee[-1]

            for instruction_instance in instruction_dict:
                if (
                    instruction_instance["fields"]["propertyprocess"]
                    == instance["new_pp_pk"]
                ):
                    old_fee = instruction_instance["fields"]["fee_agreed"]

            note = f"The agreed fee has changed from {old_fee}% to {new_fee}%"

            history_fee_agreed_change_fields["notes"] = note
            history_fee_agreed_change_fields["created"] = instance["fields"][
                "deal_change_date"
            ]
            history_fee_agreed_change_fields["type"] = "property_event"

            # Create new UUID field

            history_fee_agreed_change["pk"] = str(uuid.uuid4())

            # End create new UUID field

            # End property history fields

            history_fee_agreed_change[
                "fields"
            ] = history_fee_agreed_change_fields

            property_history_extra_dict.append(history_fee_agreed_change)

# ----------------------------------------
# SETUP
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/originals/setup.json", "r"
) as json_data:
    setup = json.load(json_data)

for instance in setup:
    if instance["pk"] == "eac112a8-c670-4d20-bb66-c4ed0329362b":
        for property_instance in property_dict:
            if property_instance["fields"]["address_line_1"] == "7 Ruston Avenue":
                property_pk = property_instance["pk"]
        for property_process_instance in propertyprocess_dict:
            if property_process_instance["fields"]["property"] == property_pk:
                instance["fields"]["propertyprocess"] = property_process_instance["pk"]

setup_dict = setup

with open(
    "/workspace/laurels-staff/common/data_dump/originals/superuser.json", "r"
) as json_data:
    super = json.load(json_data)

for instance in super:
    if instance["model"] == "users.profile":
        for hub_instance in hub_dict:
            if hub_instance["fields"]["hub_name"] == "Surrey Hub":
                dict = instance["fields"]["hub"] = []
                dict.append(hub_instance["pk"])

super_dict = super

# ----------------------------------------
# WRITE JSON
# ----------------------------------------

with open(
    "/workspace/laurels-staff/common/data_dump/new/property.json", "w"
) as json_data:
    json.dump(property_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/hub.json", "w"
) as json_data:
    json.dump(hub_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/hubtargets.json", "w"
) as json_data:
    json.dump(hub_targets, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/users.json", "w"
) as json_data:
    json.dump(custom_user_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/profile.json", "w"
) as json_data:
    json.dump(profile_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/totp.json", "w"
) as json_data:
    json.dump(totp_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/property_link.json", "w"
) as json_data:
    json.dump(property_process_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/property_history.json", "w"
) as json_data:
    json.dump(property_history_dict, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/valuation.json", "w"
) as json_data:
    json.dump(valuation_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/instruction.json", "w"
) as json_data:
    json.dump(instruction_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/instruction_letting_extra.json",
    "w",
) as json_data:
    json.dump(instruction_extra_dict, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/offer.json", "w"
) as json_data:
    json.dump(offer_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/offerer.json",
    "w",
) as json_data:
    json.dump(offerer_extra_dict, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/deal.json", "w"
) as json_data:
    json.dump(deal_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/exchangemove.json", "w"
) as json_data:
    json.dump(exchange_dict, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/salesprogression.json", "w"
) as json_data:
    json.dump(saleprogression_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/salesprogressionsettings.json",
    "w",
) as json_data:
    json.dump(salesprogressionsettings_dict, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/salesprogressionphase.json",
    "w",
) as json_data:
    json.dump(salesprogressionphase_dict, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/propertychain.json", "w"
) as json_data:
    json.dump(propertychain_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/marketing.json", "w"
) as json_data:
    json.dump(marketing_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/propertyfee.json", "w"
) as json_data:
    json.dump(property_fee_model, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/property_history_extra.json",
    "w",
) as json_data:
    json.dump(property_history_extra_dict, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/prop_history_reduction.json", "w"
) as json_data:
    json.dump(property_history_reduction_dict, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/progress_notes.json", "w"
) as json_data:
    json.dump(progress_notes_dict, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/instruction_change.json",
    "w",
) as json_data:
    json.dump(instruction_change_new_dict, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/usertargets.json",
    "w",
) as json_data:
    json.dump(user_targets_dict, json_data)

with open(
    "/workspace/laurels-staff/common/data_dump/new/reduction.json",
    "w",
) as json_data:
    json.dump(reduction_dict, json_data)


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

for object in offerer_dict:
    master_dict.append(object)

for object in offer_dict:
    master_dict.append(object)

for object in deal_dict:
    master_dict.append(object)

for object in exchange_dict:
    master_dict.append(object)

for object in salesprogression_dict:
    master_dict.append(object)

for object in salesprogressionsettings_dict:
    master_dict.append(object)

for object in salesprogressionphase_dict:
    master_dict.append(object)

for object in propertychain_dict:
    master_dict.append(object)

for object in marketing_dict:
    master_dict.append(object)

for object in propertyfee_dict:
    master_dict.append(object)

for object in property_history_extra_dict:
    master_dict.append(object)

for object in property_history_reduction_dict:
    master_dict.append(object)

for object in progress_notes_dict:
    master_dict.append(object)

for object in instruction_change_new_dict:
    master_dict.append(object)

for object in user_targets_dict:
    master_dict.append(object)

for object in reduction_dict:
    master_dict.append(object)

with open(
    "/workspace/laurels-staff/common/data_dump/master.json", "w"
) as json_data:
    json.dump(master_dict, json_data)
