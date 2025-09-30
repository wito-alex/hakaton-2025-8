from http.client import HTTPException

from rest_framework import serializers

from drf_chunked_upload.serializers import ChunkedUploadSerializer

from patient.models import Scan
from patient.upload.models import ScanUploadChunked


class ScanCreateSerializer(serializers.Serializer):
    class Meta:
        model = Scan
        fields = ("file", "name")


class ScanUploadChunkedSerializersss(ChunkedUploadSerializer):
    viewname = "upload_details"

    class Meta(ChunkedUploadSerializer.Meta):
        model = ScanUploadChunked


class ScanUploadChunkedSerializer(ChunkedUploadSerializer):
    scan = serializers.JSONField()
    viewname = "upload_details"

    class Meta(ChunkedUploadSerializer.Meta):
        model = ScanUploadChunked

    def create(self, validated_data):
        scan = Scan.objects.create()
        validated_data.pop('scan', None)
        return ScanUploadChunked.objects.create(scan=scan, **validated_data)
