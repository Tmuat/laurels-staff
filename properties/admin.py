from django.contrib import admin

from properties.models import Property


class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "postcode",
        "address_line_1",
        "address_line_2",
        "updated_by",
        "updated",
        "created_by",
        "created",
    )

    ordering = ("postcode",)

    list_filter = ("property_type", "property_style", "number_of_bedrooms")

    search_fields = ("postcode", "address_line_1")

    exclude = [
        "updated_by",
        "updated",
        "created_by",
        "created",
    ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user.get_full_name()
        obj.updated_by = request.user.get_full_name()
        super().save_model(request, obj, form, change)


admin.site.register(Property, PropertyAdmin)
