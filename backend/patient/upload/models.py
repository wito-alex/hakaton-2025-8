from django.db import models
from drf_chunked_upload.models import ChunkedUpload

from patient.models import Scan


class ScanUploadChunked(ChunkedUpload):
    scan = models.OneToOneField(Scan, models.CASCADE, verbose_name="Скан", related_name="chunked_upload")

    class Meta:
        verbose_name = "Чанк"
        verbose_name_plural = "Чанки"
