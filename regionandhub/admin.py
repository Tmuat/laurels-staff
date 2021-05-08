from django.contrib import admin

from regionandhub.models import Region


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

    search_fields = (
        "name",
    )

    exclude = [
        "updated_by",
        "updated",
        "created_by",
        "created",
    ]

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user.email
        obj.updated_by = request.user.email
        obj.save()


admin.site.register(Region, RegionAdmin)
