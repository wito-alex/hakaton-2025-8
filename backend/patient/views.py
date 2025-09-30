from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .filters import DicomInfoFilter, SliceFilter
from .models import DicomInfo, Scan, Slice
from .serializers import (
    DicomInfoSerializer,
    ScanCreateUpdateSerializer,
    ScanSerializer,
    SliceSerializer,
)


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


class HomeView(TemplateView):
    template_name = "patient/home.html"
