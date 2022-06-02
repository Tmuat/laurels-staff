from django.db import models

from common.models import Updated
from users.models import Profile


class DataIsChanged(Updated):
    class Meta:
        verbose_name = "Leaderboard Data Changed"
        verbose_name_plural = "Leaderboard Data Changed"
    
    VALUATIONS = "valuations"
    INSTRUCTIONS = "instructions"
    REDUCTIONS = "reductions"
    NEW_BUSINESS = "new_business"
    LEADERBOARD = "leaderboard"

    TYPE = [
        (VALUATIONS, "Valuations"),
        (INSTRUCTIONS, "Instructions"),
        (REDUCTIONS, "Reductions"),
        (NEW_BUSINESS, "New Business"),
        (LEADERBOARD, "Leaderboard")
    ]
    
    type = models.CharField(max_length=40, null=False, choices=TYPE)
    is_changed = models.BooleanField(default=False, null=False)

    def __str__(self):
        return type


class LastQuarterLeaderboard(Updated):
    class Meta:
        ordering = ["type", "-count"]
        verbose_name = "Leaderboard"
        verbose_name_plural = "Leaderboard"

    VALUATIONS = "valuations"
    INSTRUCTIONS = "instructions"
    REDUCTIONS = "reductions"
    NEW_BUSINESS = "new_business"

    TYPE = [
        (VALUATIONS, "Valuations"),
        (INSTRUCTIONS, "Instructions"),
        (REDUCTIONS, "Reductions"),
        (NEW_BUSINESS, "New Business")
    ]

    type = models.CharField(max_length=40, null=False, choices=TYPE)
    employee = models.ForeignKey(Profile, on_delete=models.CASCADE)
    count = models.IntegerField(null=False)
    target_percentage = models.IntegerField(null=False)

    def __str__(self):
        string = "%s (%s)" % (
                self.employee.user.abbreviated_name,
                self.type
            )
        return string
