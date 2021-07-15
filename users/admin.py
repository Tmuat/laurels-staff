from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser, Profile, UserTargets, UserTargetsByYear


class ProfileAdminInline(admin.TabularInline):
    model = Profile
    readonly_fields = [
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class UserTargetsYearAdminInline(admin.TabularInline):
    model = UserTargetsByYear
    readonly_fields = [
        "profile",
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class UserTargetsAdminInline(admin.TabularInline):
    model = UserTargets
    readonly_fields = [
        "profile_targets",
        "created",
        "created_by",
        "updated",
        "updated_by",
    ]


class CustomUserAdmin(UserAdmin):
    inlines = (
        ProfileAdminInline,
        UserTargetsAdminInline,
        UserTargetsYearAdminInline,
    )
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "email",
        "first_name",
        "last_name",
        "employee_target",
        "director",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    def employee_target(self, obj):
        return obj.profile.employee_targets

    def director(self, obj):
        return obj.profile.director

    employee_target.boolean = True
    director.boolean = True

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if not obj.pk:
                obj.created_by = request.user.get_full_name()
            obj.updated_by = request.user.get_full_name()
            super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)
