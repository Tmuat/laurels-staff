from django.contrib import admin

from home.models import LastQuarterLeaderboard, DataIsChanged


class LastQuarterLeaderboardAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "count",
        "target_percentage",
        "updated_by",
        "updated",
    ]


    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user.get_full_name()
        super().save_model(request, obj, form, change)


admin.site.register(LastQuarterLeaderboard, LastQuarterLeaderboardAdmin)


class DataIsChangedAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "is_changed",
        "updated_by",
        "updated",
    ]


    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user.get_full_name()
        super().save_model(request, obj, form, change)


admin.site.register(DataIsChanged, DataIsChangedAdmin)
