from django.contrib import admin
from django.utils.html import mark_safe

from .models import DicomInfo, Scan, Slice


@admin.register(Scan)
class AdminScan(admin.ModelAdmin):
    list_display = (
        "name",
        "work_ai_status",
        "processing_status",
        "created_at",
        "updated_at",
    )
    list_filter = ("work_ai_status", "processing_status")
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
        (None, {"fields": ("name", "path_to_study", "markup_file")}),
        ("Статусы", {"fields": ("work_ai_status", "processing_status")}),
        (
            "Детали обработки ИИ",
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
            "DICOM информация",
            {
                "classes": ("collapse",),
                "fields": ("study_uid", "series_uid"),
            },
        ),
        (
            "Временные метки",
            {"classes": ("collapse",), "fields": ("created_at", "updated_at")},
        ),
    )


class SliceInline(admin.TabularInline):
    model = Slice
    extra = 1
    can_delete = True
    show_change_link = True
    ordering = ["slice_number"]
    fields = ("slice_number", "image", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return "-"

    image_preview.short_description = "Предпросмотр"


@admin.register(DicomInfo)
class DicomInfoAdmin(admin.ModelAdmin):
    list_display = ("file_name", "scan")
    search_fields = ("file_name", "scan__name")
    list_filter = ("scan",)
    inlines = [SliceInline]


@admin.register(Slice)
class SliceAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "dicom_info",
        "slice_number",
    )
    list_filter = ("dicom_info",)
    search_fields = ("dicom_info__file_name",)
