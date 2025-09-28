from django.contrib import admin

from .models import Scan


# Register your models here.
@admin.register(Scan)
class AdminScan(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "work_ai_status",
        "processing_status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "work_ai_status", "processing_status")
    search_fields = ("name", "study_uid", "series_uid")
    ordering = ("-created_at",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "probability_of_pathology",
        "pathology",
        "time_of_processing",
    )
    fieldsets = (
        (None, {"fields": ("name", "file", "markup_file")}),
        ("Status", {"fields": ("status", "work_ai_status", "processing_status")}),
        (
            "AI Processing Details",
            {
                "classes": ("collapse",),
                "fields": (
                    "probability_of_pathology",
                    "pathology",
                    "time_of_processing",
                ),
            },
        ),
        (
            "DICOM Information",
            {
                "classes": ("collapse",),
                "fields": ("study_uid", "series_uid", "path_to_study"),
            },
        ),
        (
            "Timestamps",
            {"classes": ("collapse",), "fields": ("created_at", "updated_at")},
        ),
    )
