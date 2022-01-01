from django.contrib import admin

from boards.models import Boards


class BoardAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "propertyref",
        "updated_by",
        "updated",
        "created_by",
        "created",
    ]

    ordering = [
        "propertyprocess__property__postcode",
    ]

    search_fields = [
        "propertyprocess__property__postcode",
        "propertyprocess__property__address_line_1"
    ]

    readonly_fields = [
        "propertyref",
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


admin.site.register(Boards, BoardAdmin)
