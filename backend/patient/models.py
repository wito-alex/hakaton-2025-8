from django.db import models


class MixinCreateAt(models.Model):
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    class Meta:
        abstract = True


class MixinUpdateAt(models.Model):
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    class Meta:
        abstract = True


class Scan(MixinCreateAt, MixinUpdateAt, models.Model):
    class WorkType(models.TextChoices):
        in_work = "in_work", "В работе"
        in_processing = "in_processing", "В обработке"
        worked_out = "worked_out", "Работа закончена"

    class ProcessingStatusType(models.TextChoices):
        SUCCESS = "Success", "Успешно"
        FAILURE = "Failure", "Ошибка"

    objects = models.Manager()

    name = models.CharField(verbose_name="Название", max_length=255)
    path_to_study = models.FileField(
        verbose_name="Путь к исследованию", upload_to="uploads/scan", blank=True, null=True
    )
    markup_file = models.FileField(
        verbose_name="Файл разметки",
        upload_to="uploads/markup",
        null=True,
        blank=True,
    )
    work_ai_status = models.CharField(
        verbose_name="Статус работы ИИ",
        choices=WorkType.choices,
        default=WorkType.in_work,
        max_length=50,
    )
    study_uid = models.CharField(
        verbose_name="Уникальный идентификатор исследования",
        max_length=255,
        blank=True,
        null=True,
    )
    series_uid = models.CharField(
        verbose_name="Уникальный идентификатор серии", max_length=255, blank=True, null=True
    )
    probability_of_pathology = models.FloatField(
        verbose_name="Вероятность патологии", null=True, blank=True
    )
    pathology = models.IntegerField(
        verbose_name="Норма ли патология", null=True, blank=True
    )
    processing_status = models.CharField(
        verbose_name="Статус обработки",
        choices=ProcessingStatusType.choices,
        max_length=50,
        null=True,
        blank=True,
    )
    time_of_processing = models.FloatField(
        verbose_name="Время обработки (секунды)", null=True, blank=True
    )

    class Meta:
        verbose_name = "Скан"
        verbose_name_plural = "Сканы"

    def __str__(self):
        return self.name


class DicomInfo(models.Model):
    scan = models.ForeignKey(
        Scan, on_delete=models.CASCADE, related_name="dicom_info", verbose_name="Скан"
    )
    file_name = models.CharField(verbose_name="Название файла", max_length=255)

    class Meta:
        verbose_name = "Диком информация"
        verbose_name_plural = "Диком информация"

    def __str__(self):
        return self.file_name


class Slice(models.Model):
    dicom_info = models.ForeignKey(
        DicomInfo,
        on_delete=models.CASCADE,
        related_name="slices",
        verbose_name="Информация Dicom",
    )
    slice_number = models.IntegerField(verbose_name="Номер среза")
    image = models.ImageField(
        verbose_name="Фото среза", upload_to="uploads/slices/", blank=True, null=True
    )
    probability = models.FloatField(verbose_name="Вероятность", null=True, blank=True)

    class Meta:
        verbose_name = "Срез"
        verbose_name_plural = "Срезы"
        ordering = ["slice_number"]

    def __str__(self):
        return f"Срез {self.slice_number} для {self.dicom_info.file_name}"
