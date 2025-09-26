from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .upload.views import ScanUploadChunkedView
from .views import ScanViewSet

router = DefaultRouter()
router.register(r"scans", ScanViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("scans/upload/", ScanUploadChunkedView.as_view(), name="scan-upload"),
    path(
        "scans/upload/<int:pk>/",
        ScanUploadChunkedView.as_view(),
        name="scan-upload-detail",
    ),
]
