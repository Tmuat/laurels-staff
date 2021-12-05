from django.contrib import admin

from touts.models import (
    Area,
    ToutProperty,
    Landlord,
    ToutLetter
)


class AreaAdmin(admin.ModelAdmin):
    list_display = [
        "area_code",
        "is_active",
        "updated_by",
        "updated",
        "created_by",
        "created",
    ]

    ordering = [
        "area_code",
    ]

    search_fields = ["area_code"]

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


admin.site.register(Area, AreaAdmin)


class ToutPropertyAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "postcode",
        "address_line_1",
        "address_line_2",
        "area",
        "updated_by",
        "updated",
        "created_by",
        "created",
    ]

    ordering = [
        "postcode",
        "address_line_1"
    ]

    search_fields = [
        "postcode",
        "address_line_1"
    ]

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


admin.site.register(ToutProperty, ToutPropertyAdmin)


class ToutLetterAdminInline(admin.TabularInline):
    model = ToutLetter
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class LandlordAdmin(admin.ModelAdmin):
    inlines = [
        ToutLetterAdminInline
    ]

    list_display = [
        "__str__",
        "address_line_1",
        "postcode",
    ]

    ordering = [
        "landlord_property__postcode",
    ]

    search_fields = [
        "landlord_property__postcode",
        "landlord_property__address_line_1"
    ]

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

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if not obj.pk:
                obj.created_by = request.user.get_full_name()
            obj.updated_by = request.user.get_full_name()
            super().save_model(request, obj, form, change)


admin.site.register(Landlord, LandlordAdmin)
