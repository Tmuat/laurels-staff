from django.contrib import admin

from weekends.models import WeekendDays


class WeekendDaysAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "title",
        "start",
        "end",
    ]

    ordering = [
        "start",
    ]

    list_filter = [
        "hub",
    ]

    search_fields = ["title"]


admin.site.register(WeekendDays, WeekendDaysAdmin)
