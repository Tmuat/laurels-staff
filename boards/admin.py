from django.contrib import admin

from boards.models import Boards, BoardsInfo


class BoardsInfoAdminInline(admin.StackedInline):
    model = BoardsInfo
    readonly_fields = [
        "activate_date",
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class BoardAdmin(admin.ModelAdmin):
    inlines = [
        BoardsInfoAdminInline
    ]

    list_display = [
        "__str__",
        "propertyref",
        "signmaster_id",
        "created_on_signmaster",
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
        "propertyprocess",
        "propertyref",
        "signmaster_id",
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


admin.site.register(Boards, BoardAdmin)
