from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "disease",
        "result",
        "probability",
        "created_at",
    )

    list_filter = (
        "disease",
        "result",
    )

    search_fields = (
        "user__username",
        "disease",
    )

    ordering = ("-created_at",)