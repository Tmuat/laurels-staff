from django.contrib import admin

from invitations.models import UserInvitations
from users.models import UserTargetsByYear, UserTargets


class UserTargetsYearAdminInline(admin.TabularInline):
    model = UserTargetsByYear
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class UserTargetsAdminInline(admin.TabularInline):
    model = UserTargets
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class InvitationAdmin(admin.ModelAdmin):
    inlines = (
        UserTargetsAdminInline,
        UserTargetsYearAdminInline,
    )
    model = UserInvitations
    list_display = (
        "email",
        "invited",
        "accepted",
        "first_name",
        "last_name",
    )
    readonly_fields = [
        "key",
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]
    list_filter = ("is_staff", "accepted")
    search_fields = ("email",)
    ordering = ("invited",)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user.get_full_name()
        obj.updated_by = request.user.get_full_name()
        super().save_model(request, obj, form, change)


admin.site.register(UserInvitations, InvitationAdmin)
