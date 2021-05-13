from django.contrib import admin

from regionandhub.models import Region, Hub, HubTargets, HubTargetsYear


class RegionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "is_active",
        "created",
        "created_by",
        "updated",
        "updated_by",
    )

    ordering = ("name",)

    list_filter = ("is_active",)

    prepopulated_fields = {"slug": ("name",)}

    search_fields = ("name",)

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


admin.site.register(Region, RegionAdmin)


class HubTargetsYearAdminInline(admin.TabularInline):
    model = HubTargetsYear
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class HubTargetsAdminInline(admin.TabularInline):
    model = HubTargets
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class HubAdmin(admin.ModelAdmin):
    inlines = (HubTargetsAdminInline, HubTargetsYearAdminInline)
    list_display = (
        "hub_name",
        "slug",
        "region",
        "is_active",
        "created",
        "created_by",
        "updated",
        "updated_by",
    )

    ordering = ("hub_name",)

    list_filter = ("is_active", "region")

    prepopulated_fields = {"slug": ("hub_name",)}

    search_fields = ("hub_name",)

    readonly_fields = [
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

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if not obj.pk:
                obj.created_by = request.user.get_full_name()
            obj.updated_by = request.user.get_full_name()
            super().save_model(request, obj, form, change)


admin.site.register(Hub, HubAdmin)
