from rest_framework import viewsets
from .models import Scan
from .serializers import ScanSerializer


class ScanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows scans to be viewed or edited.
    """
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer
