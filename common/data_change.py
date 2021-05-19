import json
import uuid


# exec(open('common/data_change.py').read())

with open(
    "/workspace/laurels-staff/common/data_dump/property.json", "r"
) as json_data:
    property_model = json.load(json_data)  # deserialises it
    # data2 = json.dumps(data1) # json formatted string

for prop in property_model:

    # Changing the model to new value

    prop["model"] = "properties.property"

    # End changing the model to new value

    # Changing the property type to new values

    if prop["fields"]["property_type"] == "House - Terraced":
        prop["fields"]["property_type"] = "house_terraced"

    elif prop["fields"]["property_type"] == "House - End of Terrace":
        prop["fields"]["property_type"] = "house_end_terrace"

    elif prop["fields"]["property_type"] == "House - Semi-Detached":
        prop["fields"]["property_type"] = "house_semi_detached"

    elif prop["fields"]["property_type"] == "House - Detached":
        prop["fields"]["property_type"] = "house_detached"

    elif prop["fields"]["property_type"] == "Maisonette - Ground Floor":
        prop["fields"]["property_type"] = "maisonette_ground_floor"

    elif prop["fields"]["property_type"] == "Maisonette - Top Floor":
        prop["fields"]["property_type"] = "maisonette_top_floor"

    elif prop["fields"]["property_type"] == "Flat - Ground Floor":
        prop["fields"]["property_type"] = "flat_ground_floor"

    elif prop["fields"]["property_type"] == "Flat - Upper Floors":
        prop["fields"]["property_type"] = "flat_upper_floor"

    elif prop["fields"]["property_type"] == "Bungalow - Semi-Detached":
        prop["fields"]["property_type"] = "bungalow_semi_detached"

    elif prop["fields"]["property_type"] == "Bungalow - Detached":
        prop["fields"]["property_type"] = "bungalow_detached"

    elif prop["fields"]["property_type"] == "Commercial":
        prop["fields"]["property_type"] = "commercial"

    elif prop["fields"]["property_type"] == "Land":
        prop["fields"]["property_type"] = "land"

    elif prop["fields"]["property_type"] == "Other":
        prop["fields"]["property_type"] = "other"

    # End change property type

    # Changing the property style to new values

    if prop["fields"]["property_style"] == "Modern":
        prop["fields"]["property_style"] = "modern"

    elif prop["fields"]["property_style"] == "New Build":
        prop["fields"]["property_style"] = "new_build"

    elif prop["fields"]["property_style"] == "Period":
        prop["fields"]["property_style"] = "period"

    # End change property style

    # Changing the property tenure to new values

    if prop["fields"]["tenure"] == "Freehold":
        prop["fields"]["tenure"] = "freehold"

    elif prop["fields"]["tenure"] == "Leasehold":
        prop["fields"]["tenure"] = "leasehold"

    elif prop["fields"]["tenure"] == "Share of Freehold":
        prop["fields"]["tenure"] = "share_of_freehold"

    # End change property tenure

    # Add new fields

    prop["fields"]["created_by"] = "Admin"
    prop["fields"]["created"] = "2000-01-13T13:13:13.000Z"
    prop["fields"]["updated_by"] = "Admin"
    prop["fields"]["updated"] = "2000-01-13T13:13:13.000Z"

    # End add new fields

    # Move original PK

    prop["old_pk"] = prop["pk"]

    # End move original PK

    # Create new UUID field

    prop["pk"] = str(uuid.uuid4())

with open(
    "/workspace/laurels-staff/common/data_dump/property.json", "w"
) as json_data:
    json.dump(property_model, json_data)


with open(
    "/workspace/laurels-staff/common/data_dump/property_process.json", "r"
) as json_data:
    property_process_model = json.load(json_data)  # deserialises it
    # data2 = json.dumps(data1) # json formatted string

for prop in property_process_model:

    # Changing the model to new value

    prop["model"] = "properties.property"

    # End changing the model to new value

    # Changing the property type to new values

    if prop["fields"]["property_type"] == "House - Terraced":
        prop["fields"]["property_type"] = "house_terraced"

    elif prop["fields"]["property_type"] == "House - End of Terrace":
        prop["fields"]["property_type"] = "house_end_terrace"

    elif prop["fields"]["property_type"] == "House - Semi-Detached":
        prop["fields"]["property_type"] = "house_semi_detached"

    elif prop["fields"]["property_type"] == "House - Detached":
        prop["fields"]["property_type"] = "house_detached"

    elif prop["fields"]["property_type"] == "Maisonette - Ground Floor":
        prop["fields"]["property_type"] = "maisonette_ground_floor"

    elif prop["fields"]["property_type"] == "Maisonette - Top Floor":
        prop["fields"]["property_type"] = "maisonette_top_floor"

    elif prop["fields"]["property_type"] == "Flat - Ground Floor":
        prop["fields"]["property_type"] = "flat_ground_floor"

    elif prop["fields"]["property_type"] == "Flat - Upper Floors":
        prop["fields"]["property_type"] = "flat_upper_floor"

    elif prop["fields"]["property_type"] == "Bungalow - Semi-Detached":
        prop["fields"]["property_type"] = "bungalow_semi_detached"

    elif prop["fields"]["property_type"] == "Bungalow - Detached":
        prop["fields"]["property_type"] = "bungalow_detached"

    elif prop["fields"]["property_type"] == "Commercial":
        prop["fields"]["property_type"] = "commercial"

    elif prop["fields"]["property_type"] == "Land":
        prop["fields"]["property_type"] = "land"

    elif prop["fields"]["property_type"] == "Other":
        prop["fields"]["property_type"] = "other"

    # End change property type

    # Changing the property style to new values

    if prop["fields"]["property_style"] == "Modern":
        prop["fields"]["property_style"] = "modern"

    elif prop["fields"]["property_style"] == "New Build":
        prop["fields"]["property_style"] = "new_build"

    elif prop["fields"]["property_style"] == "Period":
        prop["fields"]["property_style"] = "period"

    # End change property style

    # Changing the property tenure to new values

    if prop["fields"]["tenure"] == "Freehold":
        prop["fields"]["tenure"] = "freehold"

    elif prop["fields"]["tenure"] == "Leasehold":
        prop["fields"]["tenure"] = "leasehold"

    elif prop["fields"]["tenure"] == "Share of Freehold":
        prop["fields"]["tenure"] = "share_of_freehold"

    # End change property tenure

    # Add new fields

    prop["fields"]["created_by"] = "Admin"
    prop["fields"]["created"] = "2000-01-13T13:13:13.000Z"
    prop["fields"]["updated_by"] = "Admin"
    prop["fields"]["updated"] = "2000-01-13T13:13:13.000Z"

    # End add new fields

    # Move original PK

    prop["old_pk"] = prop["pk"]

    # End move original PK

    # Create new UUID field

    prop["pk"] = str(uuid.uuid4())

with open(
    "/workspace/laurels-staff/common/data_dump/property.json", "w"
) as json_data:
    json.dump(data1, json_data)
