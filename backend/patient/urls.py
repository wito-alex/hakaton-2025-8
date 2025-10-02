from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .upload.views import ScanUploadChunkedView
from .views import (DicomInfoViewSet, ExportScansExcelView, HomeView,
                    ScanViewSet, SliceViewSet)

router = DefaultRouter()
router.register(r"scans", ScanViewSet)
router.register(r"slices", SliceViewSet)
router.register(r"dicom-info", DicomInfoViewSet)

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("scans/upload/", ScanUploadChunkedView.as_view(), name="upload_data"),
    path(
        "scan/upload/<str:pk>/", ScanUploadChunkedView.as_view(), name="upload_details"
    ),
    path(
        "scan/upload/complete/", ScanUploadChunkedView.as_view(), name="upload_compete"
    ),
    path("scans/export/", ExportScansExcelView.as_view(), name="export-scans-excel"),
    path("", include(router.urls)),
]
