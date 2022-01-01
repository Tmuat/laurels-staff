from django import forms


class AddNewBoardForm(forms.Form):
    vendor_name = forms.CharField(
        strip=True,
        widget=forms.TextInput(
            attrs={
                'required': True
            }
        ),
        label="Vendor Name"
    )


#     vendorname = SubElement(movement, "vendorname")
#     vendorname.text = "T Muat"
#     boardtypeid = SubElement(movement, "boardtypeid")
#     boardtypeid.text = "42462"
#     movementtypeid = SubElement(movement, "movementtypeid")
#     movementtypeid.text = "1"
#     boardstatusid = SubElement(movement, "boardstatusid")
#     boardstatusid.text = "1"
#     noofboards = SubElement(movement, "noofboards")
#     noofboards.text = "1"
#     houseno = SubElement(movement, "houseno")
#     houseno.text = "Flat 5"
#     address1 = SubElement(movement, "address1")
#     address1.text = "Woodfield Court"
#     address2 = SubElement(movement, "address2")
#     address2.text = "Woodfield Avenue"
#     locality = SubElement(movement, "locality")
#     locality.text = ""
#     town = SubElement(movement, "town")
#     town.text = "Rugby"
#     county = SubElement(movement, "county")
#     county.text = "Warwickshire"
#     postcode = SubElement(movement, "postcode")
#     postcode.text = "CV22 5HT"
#     agentnotes = SubElement(movement, "agentnotes")
#     agentnotes.text = "Please erect to the side of the house."
