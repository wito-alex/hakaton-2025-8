from rest_framework import permissions

from drf_chunked_upload.views import ChunkedUploadView
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema

from .models import ScanUploadChunked
from .serializers import ScanUploadChunkedSerializer, ScanUploadChunkedSerializersss


class ScanUploadChunkedView(ChunkedUploadView):
    model = ScanUploadChunked
    serializer_class = ScanUploadChunkedSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return super().get_queryset()

    @extend_schema(
        summary="Put [ScanUploadChunked]",
        description=(
            "Put ScanUploadChunked."
            "Will not work via swagger. Since you need to pass the file and the Content-Range tag"
        ),
        responses={200: ScanUploadChunkedSerializersss},
        parameters=[
            OpenApiParameter(
                name="Content-Range",
                type=str,
                location=OpenApiParameter.HEADER,
                examples=[
                    OpenApiExample(
                        "Header example",
                        description="file size",
                        value="bytes 0-100/100",
                    ),
                ],
            ),
        ],
    )
    def put(self, request, pk=None, *args, **kwargs):
        return super().put(request, pk=pk, *args, **kwargs)

    @property
    def response_serializer_class(self):
        serializer_class = ScanUploadChunkedSerializersss
        if self.request is None or self.request.method not in ["PUT", "POST"]:
            serializer_class = ScanUploadChunkedSerializersss
        return serializer_class

    def post(self, request, pk=None, *args, **kwargs):
        data = super().post(request, pk, *args, **kwargs)

        chunked_upload = self.get_object()
        scan_instance = chunked_upload.scan
        scan_instance.file = chunked_upload.file
        scan_instance.save(update_fields=['file'])

        return data
