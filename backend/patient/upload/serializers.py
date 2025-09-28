from rest_framework import serializers

from drf_chunked_upload.serializers import ChunkedUploadSerializer

from patient.models import Scan
from patient.upload.models import ScanUploadChunked


class ScanCreateSerializer(serializers.Serializer):
    class Meta:
        model = Scan
        fields = ("file", "name")


class ScanUploadChunkedSerializersss(ChunkedUploadSerializer):
    viewname = "scan-upload-detail"

    class Meta(ChunkedUploadSerializer.Meta):
        model = ScanUploadChunked


class ScanUploadChunkedSerializer(ChunkedUploadSerializer):
    scan = serializers.JSONField()
    viewname = "scan-upload-detail"

    def create(self, validated_data):
        scan_data = validated_data.pop("scan")
        scan = Scan.objects.create(**scan_data)
        return ScanUploadChunked.objects.create(scan=scan, **validated_data)
