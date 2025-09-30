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
    class StatusType(models.TextChoices):
        preparing_for_viewing = (
            "preparing_for_viewing",
            "Подготовка к просмотру:#3F391A:#EEE6BE",
        )
        ready_to_watch = "ready_to_watch", "Готов к просмотру:#0078E7:#BED7EE"
        ai_processing_completed = (
            "ai_processing_completed",
            "Завершена обработка ИИ:#057306:#D7FCD7",
        )
        in_processing = "in_processing", "В обработке ИИ:#381BEB:#ECE9FD"
        viewed = "viewed", "Просмотрен:#6D06C6:#F3E8FF"
        adjusted_by_user = (
            "adjusted_by_user",
            "Скорректирован пользователем:#8B7500:#FEF8C3",
        )

    class WorkType(models.TextChoices):
        in_work = "in_work", "В работе"
        in_processing = "in_processing", "В обработке"
        worked_out = "worked_out", "Работа закончена"

    class ProcessingStatusType(models.TextChoices):
        SUCCESS = "Success", "Успешно"
        FAILURE = "Failure", "Ошибка"

    objects = models.Manager()

    name = models.CharField(verbose_name="Название", max_length=255)
    file = models.FileField(
        verbose_name="Файл", upload_to="uploads/scan", blank=True, null=True
    )
    status = models.CharField(
        verbose_name="Статус",
        choices=StatusType.choices,
        default=StatusType.preparing_for_viewing,
        max_length=50,
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
        verbose_name="Уникальный идентификатор исследования", max_length=255, blank=True, null=True
    )
    series_uid = models.CharField(
        verbose_name="Уникальный идентификатор серии", max_length=255, blank=True, null=True
    )
    path_to_study = models.CharField(
        verbose_name="Путь к исследованию", max_length=255, null=True, blank=True
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
