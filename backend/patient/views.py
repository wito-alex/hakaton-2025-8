from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from drf_spectacular.utils import extend_schema

from .models import Scan
from .serializers import ScanCreateUpdateSerializer, ScanSerializer


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
