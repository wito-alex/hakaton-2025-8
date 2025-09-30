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
    scan = serializers.PrimaryKeyRelatedField(read_only=True)
    viewname = "upload_details"

    class Meta(ChunkedUploadSerializer.Meta):
        model = ScanUploadChunked

    def create(self, validated_data):
        # Автоматически создаем новый объект Scan при начале загрузки
        scan = Scan.objects.create(name=validated_data.get('filename'))
        # Создаем объект чанковой загрузки и связываем его с новым Scan
        return ScanUploadChunked.objects.create(scan=scan, **validated_data)
