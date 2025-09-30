from rest_framework import serializers

from .models import DicomInfo, Scan, Slice


class SliceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slice
        fields = "__all__"


class DicomInfoSerializer(serializers.ModelSerializer):
    slices = SliceSerializer(many=True, read_only=True)

    class Meta:
        model = DicomInfo
        fields = ["id", "scan", "file_name", "slices"]


class ScanSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    work_ai_status = serializers.CharField(source="get_work_ai_status_display")
    processing_status = serializers.CharField(source="get_processing_status_display")

    class Meta:
        model = Scan
        fields = "__all__"


class ScanCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ("name", "file", "markup_file")
