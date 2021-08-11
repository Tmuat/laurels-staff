from django.contrib import admin

from lettings.models import (
    LettingProperties,
    Renewals,
    SecondTwelve,
    EPC,
    Gas,
    Electrical
)


class GasAdminInline(admin.TabularInline):
    model = Gas
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class EPCAdminInline(admin.TabularInline):
    model = EPC
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class ElectricalAdminInline(admin.TabularInline):
    model = Electrical
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class SecondTwelveAdminInline(admin.TabularInline):
    model = SecondTwelve
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class RenewalsAdminInline(admin.TabularInline):
    model = Renewals
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class LettingPropertiesAdmin(admin.ModelAdmin):
    inlines = [
        RenewalsAdminInline,
        SecondTwelveAdminInline,
        ElectricalAdminInline,
        EPCAdminInline,
        GasAdminInline
    ]

    list_display = [
        "__str__",
        "lettings_service_level",
        "is_active",
    ]

    list_filter = ["is_active", "lettings_service_level",]

    readonly_fields = [
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


admin.site.register(LettingProperties, LettingPropertiesAdmin)
