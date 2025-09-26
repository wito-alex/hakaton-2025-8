from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Scan


class ScanSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    work_ai_status = serializers.CharField(source='get_work_ai_status_display')
    processing_status = serializers.CharField(source='get_processing_status_display')

    class Meta:
        model = Scan
        fields = '__all__'
