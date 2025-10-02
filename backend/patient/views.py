from django.views.generic import TemplateView
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from django.http import HttpResponse
from openpyxl import Workbook
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .filters import DicomInfoFilter, SliceFilter
from .models import DicomInfo, Scan, Slice
from .serializers import (
    DicomInfoSerializer,
    ScanCreateUpdateSerializer,
    ScanSerializer,
    SliceSerializer,
)


@extend_schema(
    summary="Export Scans to Excel",
    description="""
    Создает и возвращает Excel (.xlsx) файл с данными по указанным сканам.

    Принимает POST-запрос с ID сканов.
    В теле запроса нужно передать `scan_ids` как список ID.
    Например, используя form-data:
    - `scan_ids`: 1
    - `scan_ids`: 2
    """,
    parameters=[
        OpenApiParameter(
            name='scan_ids',
            type={'type': 'array', 'items': {'type': 'integer'}},
            location=OpenApiParameter.QUERY,
            required=True,
            description='Список ID сканов для экспорта.'
        )
    ],
    responses={
        200: OpenApiTypes.BINARY,
        400: OpenApiTypes.STR,
    }
)
class ExportScansExcelView(APIView):
    def post(self, request, *args, **kwargs):
        scan_ids = request.query_params.getlist('scan_ids')
        if not scan_ids:
            return HttpResponse("No scan IDs provided", status=400)

        scans = Scan.objects.filter(id__in=scan_ids)

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Scans Report"

        headers = [
            "path_to_study",
            "study_uid",
            "series_uid",
            "probability_of_pathology",
            "pathology",
            "processing_status",
            "time_of_processing",
        ]
        sheet.append(headers)

        for scan in scans:
            full_url = request.build_absolute_uri(scan.path_to_study.url) if scan.path_to_study else ""
            row = [
                full_url,
                scan.study_uid,
                scan.series_uid,
                scan.probability_of_pathology,
                scan.pathology,
                scan.processing_status,
                scan.time_of_processing,
            ]
            sheet.append(row)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=scans_report.xlsx"
        workbook.save(response)

        return response


class DicomInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing DicomInfo.
    """

    queryset = DicomInfo.objects.all().prefetch_related("slices")
    serializer_class = DicomInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DicomInfoFilter


class SliceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing Slices.
    """

    queryset = Slice.objects.all()
    serializer_class = SliceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SliceFilter


class ScanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows scans to be viewed or edited.
    """

    queryset = Scan.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ScanCreateUpdateSerializer
        return ScanSerializer

    @extend_schema(
        request=ScanCreateUpdateSerializer,
        responses={201: ScanSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=ScanCreateUpdateSerializer,
        responses={200: ScanSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def process_with_ai(self, request, pk=None):
        """
        Запускает асинхронную задачу обработки скана с помощью AI.
        """
        try:
            scan = self.get_object()
            if not scan.file:
                return Response({'error': 'Scan has no file to process.'}, status=status.HTTP_400_BAD_REQUEST)

            # Запускаем задачу в Celery
            process_scan_with_ai.delay(scan.id)

            scan.work_ai_status = Scan.WorkType.in_work
            scan.save()

            return Response({'status': 'AI processing started'}, status=status.HTTP_202_ACCEPTED)
        except Scan.DoesNotExist:
            return Response({'error': 'Scan not found.'}, status=status.HTTP_404_NOT_FOUND)


class HomeView(TemplateView):
    template_name = "patient/home.html"
