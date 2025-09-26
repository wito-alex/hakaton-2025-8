from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScanViewSet
from .upload.views import ScanUploadChunkedView

router = DefaultRouter()
router.register(r'scans', ScanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('scans/upload/', ScanUploadChunkedView.as_view(), name='scan-upload'),
    path('scans/upload/<int:pk>/', ScanUploadChunkedView.as_view(), name='scan-upload-detail'),
]
