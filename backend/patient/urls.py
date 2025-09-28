from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .upload.views import ScanUploadChunkedView
from .views import HomeView, ScanViewSet

router = DefaultRouter()
router.register(r"scans", ScanViewSet)

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("", include(router.urls)),
    path("scans/upload/", ScanUploadChunkedView.as_view(), name="scan-upload"),
    path("scan/upload/<str:pk>/", ScanUploadChunkedView.as_view(), name="upload_details"),
    path("scan/upload/complete/", ScanUploadChunkedView.as_view(), name="upload_compete"),
]
