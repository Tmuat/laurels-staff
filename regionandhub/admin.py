from django.contrib import admin

from regionandhub.models import Region, Hub


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
        if not obj.created_by:
            obj.created_by = request.user.get_full_name()
        obj.updated_by = request.user.get_full_name()
        obj.save()


admin.site.register(Region, RegionAdmin)


class HubAdmin(admin.ModelAdmin):
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

    exclude = [
        "updated_by",
        "updated",
        "created_by",
        "created",
    ]

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user.get_full_name()
        obj.updated_by = request.user.get_full_name()
        obj.save()


admin.site.register(Hub, HubAdmin)
