from django.contrib import admin

from properties.models import (
    Property,
    PropertyProcess,
    PropertyHistory,
    Valuation,
    Instruction,
    InstructionChange,
    InstructionLettingsExtra,
    OffererDetails,
    OffererMortgage,
    OffererCash,
    OffererDetailsLettings,
    Offer,
    Deal,
    ExchangeMove,
    SalesProgression,
    SalesProgressionSettings,
    SalesProgressionPhase,
    PropertyChain,
    Marketing,
    PropertyFees,
    ProgressionNotes,
    PropertySellingInformation,
    Reduction,
    LettingsProgression,
    LettingsProgressionPhase,
    LettingsProgressionSettings,
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


class InstructionChangeAdminInline(admin.TabularInline):
    model = InstructionChange
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


class OffererDetailsLettingsAdminInline(admin.TabularInline):
    model = OffererDetailsLettings
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class OfferAdminInline(admin.TabularInline):
    model = Offer
    readonly_fields = [
        "offerer_lettings_details",
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


class ReductionAdminInline(admin.TabularInline):
    model = Reduction
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class SalesProgressionAdminInline(admin.StackedInline):
    model = SalesProgression
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class LettingsProgressionAdminInline(admin.StackedInline):
    model = LettingsProgression
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class MarketingAdminInline(admin.StackedInline):
    model = Marketing
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class PropertyFeeAdminInline(admin.TabularInline):
    model = PropertyFees
    readonly_fields = [
        "new_business",
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class ProgressionNotesAdminInline(admin.TabularInline):
    model = ProgressionNotes
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class PropertySellingInformationAdminInline(admin.StackedInline):
    model = PropertySellingInformation
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class PropertyChainAdminInline(admin.TabularInline):
    model = PropertyChain
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class PropertyProcessAdmin(admin.ModelAdmin):
    inlines = [
        PropertyFeeAdminInline,
        PropertyHistoryAdminInline,
        ValuationAdminInline,
        InstructionAdminInline,
        InstructionChangeAdminInline,
        InstructionLettingsExtraAdminInline,
        OffererDetailsAdminInline,
        OffererDetailsLettingsAdminInline,
        OfferAdminInline,
        DealAdminInline,
        ExchangeAdminInline,
        SalesProgressionAdminInline,
        LettingsProgressionAdminInline,
        ProgressionNotesAdminInline,
        PropertySellingInformationAdminInline,
        MarketingAdminInline,
        PropertyChainAdminInline,
        ReductionAdminInline,
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


class PropertyFeeAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "date",
        "new_business",
        "price",
        "fee",
        "active",
    ]

    ordering = ["propertyprocess__property__postcode", "-date"]

    list_filter = [
        "date",
    ]

    search_fields = [
        "propertyprocess__property__postcode",
        "propertyprocess__property__address_line_1",
    ]

    readonly_fields = [
        "new_business",
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user.get_full_name()
        obj.updated_by = request.user.get_full_name()
        super().save_model(request, obj, form, change)


admin.site.register(PropertyFees, PropertyFeeAdmin)


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
        "offerer_details",
        "offerer_lettings_details",
        "propertyprocess",
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
        "full_name",
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


class OffersLettingsAdminInline(admin.TabularInline):
    model = Offer
    readonly_fields = [
        "offerer_details",
        "offerer_lettings_details",
        "propertyprocess",
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class OffererDetailsLettingsAdmin(admin.ModelAdmin):
    inlines = [
        OffersLettingsAdminInline,
    ]

    list_display = [
        "__str__",
        "completed_offer_form",
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


admin.site.register(OffererDetailsLettings, OffererDetailsLettingsAdmin)


class SalesProgressionPhaseAdminInline(admin.TabularInline):
    model = SalesProgressionPhase
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class SalesProgressionSettingsAdminInline(admin.TabularInline):
    model = SalesProgressionSettings
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class SalesProgressionAdmin(admin.ModelAdmin):
    inlines = [
        SalesProgressionPhaseAdminInline,
        SalesProgressionSettingsAdminInline,
    ]

    list_display = [
        "__str__",
        "get_phase",
    ]

    ordering = [
        "propertyprocess__property__postcode",
        "propertyprocess__property__address_line_1",
    ]

    list_filter = [
        "propertyprocess__hub",
    ]

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

    def get_phase(self, obj):
        phase = obj.sales_progression_phase.get_overall_phase_display()
        if phase == 0:
            phase = "No Phase Complete"
        return phase

    get_phase.short_description = "Sales Progression Phase"


admin.site.register(SalesProgression, SalesProgressionAdmin)


class LettingsProgressionPhaseAdminInline(admin.TabularInline):
    model = LettingsProgressionPhase
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class LettingsProgressionSettingsAdminInline(admin.TabularInline):
    model = LettingsProgressionSettings
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class LettingsProgressionAdmin(admin.ModelAdmin):
    inlines = [
        LettingsProgressionPhaseAdminInline,
        LettingsProgressionSettingsAdminInline,
    ]

    list_display = [
        "__str__",
        "get_phase",
    ]

    ordering = [
        "propertyprocess__property__postcode",
        "propertyprocess__property__address_line_1",
    ]

    list_filter = [
        "propertyprocess__hub",
    ]

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

    def get_phase(self, obj):
        phase = obj.lettings_progression_phase.get_overall_phase_display()
        if phase == 0:
            phase = "No Phase Complete"
        return phase

    get_phase.short_description = "Lettings Progression Phase"


admin.site.register(LettingsProgression, LettingsProgressionAdmin)
