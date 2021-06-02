from django.contrib import admin

from properties.models import (
    Property,
    PropertyProcess,
    PropertyHistory,
    Valuation,
    Instruction,
    InstructionLettingsExtra,
    OffererDetails,
    OffererMortgage,
    OffererCash,
    Offer,
    Deal,
    ExchangeMove,
    SaleStatus,
    SaleStatusSettings,
    SaleStatusPhase,
)


class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "postcode",
        "address_line_1",
        "address_line_2",
        "updated_by",
        "updated",
        "created_by",
        "created",
    ]

    ordering = [
        "postcode",
    ]

    list_filter = ["property_type", "property_style", "number_of_bedrooms"]

    search_fields = ["postcode", "address_line_1"]

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


admin.site.register(Property, PropertyAdmin)


class PropertyHistoryAdminInline(admin.TabularInline):
    model = PropertyHistory
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class ValuationAdminInline(admin.TabularInline):
    model = Valuation
    readonly_fields = [
        "date",
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class InstructionAdminInline(admin.TabularInline):
    model = Instruction
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class InstructionLettingsExtraAdminInline(admin.TabularInline):
    model = InstructionLettingsExtra
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class OffererDetailsAdminInline(admin.TabularInline):
    model = OffererDetails
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class OfferAdminInline(admin.TabularInline):
    model = Offer
    readonly_fields = [
        "offerer_details",
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class DealAdminInline(admin.TabularInline):
    model = Deal
    readonly_fields = [
        "offer_accepted",
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class ExchangeAdminInline(admin.TabularInline):
    model = ExchangeMove
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class SaleStatusAdminInline(admin.StackedInline):
    model = SaleStatus
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class PropertyProcessAdmin(admin.ModelAdmin):
    inlines = [
        PropertyHistoryAdminInline,
        ValuationAdminInline,
        InstructionAdminInline,
        InstructionLettingsExtraAdminInline,
        OffererDetailsAdminInline,
        OfferAdminInline,
        DealAdminInline,
        ExchangeAdminInline,
        SaleStatusAdminInline,
    ]

    list_display = [
        "__str__",
        "employee",
        "sector",
        "hub",
        "macro_status",
        "legacy_property",
    ]

    ordering = [
        "property__postcode",
    ]

    list_filter = ["sector", "hub", "employee"]

    search_fields = ["property__postcode", "property__address_line_1"]

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


admin.site.register(PropertyProcess, PropertyProcessAdmin)


class OffererMortgageAdminInline(admin.TabularInline):
    model = OffererMortgage
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class OffererCashAdminInline(admin.TabularInline):
    model = OffererCash
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class OffersAdminInline(admin.TabularInline):
    model = Offer
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class OffererDetailsAdmin(admin.ModelAdmin):
    inlines = [
        OffererMortgageAdminInline,
        OffererCashAdminInline,
        OffersAdminInline,
    ]

    list_display = [
        "__str__",
        "completed_offer_form",
        "funding",
    ]

    ordering = [
        "propertyprocess__property__postcode",
        "propertyprocess__property__address_line_1",
        "full_name",
    ]

    list_filter = ["propertyprocess__sector", "propertyprocess__hub"]

    search_fields = [
        "propertyprocess__property__postcode",
        "propertyprocess__property__address_line_1",
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


admin.site.register(OffererDetails, OffererDetailsAdmin)


class SaleStatusPhaseAdminInline(admin.TabularInline):
    model = SaleStatusPhase
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class SaleStatusSettingsAdminInline(admin.TabularInline):
    model = SaleStatusSettings
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class SaleStatusAdmin(admin.ModelAdmin):
    inlines = [
        SaleStatusPhaseAdminInline,
        SaleStatusSettingsAdminInline,
    ]

    list_display = [
        "__str__",
    ]

    ordering = [
        "propertyprocess__property__postcode",
        "propertyprocess__property__address_line_1",
    ]

    list_filter = ["propertyprocess__hub"]

    search_fields = [
        "propertyprocess__property__postcode",
        "propertyprocess__property__address_line_1",
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


admin.site.register(SaleStatus, SaleStatusAdmin)
