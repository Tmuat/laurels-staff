from django.contrib import admin

from invitations.models import UserInvitations


class InvitationAdmin(admin.ModelAdmin):
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
