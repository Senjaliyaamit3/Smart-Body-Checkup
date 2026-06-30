from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "age",
        "gender",
        "phone",
        "blood_group",
    )

    search_fields = ("user__username", "phone")