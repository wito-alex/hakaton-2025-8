from django_filters import rest_framework as filters

from .models import DicomInfo, Slice


# Кастомный фильтр для приема ID, разделенных запятыми (напр. "1,2,3")
class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class DicomInfoFilter(filters.FilterSet):
    class Meta:
        model = DicomInfo
        fields = {
            "scan": ["exact"],
        }


class SliceFilter(filters.FilterSet):
    # Новый фильтр для списка ID. Пример: /api/patient/slices/?dicom_info_in=1,2,3
    dicom_info_in = NumberInFilter(field_name="dicom_info_id", lookup_expr="in")

    # Новый фильтр для получения срезов по ID скана. Пример: /api/patient/slices/?scan=1
    scan = filters.NumberFilter(field_name="dicom_info__scan_id")

    class Meta:
        model = Slice
        fields = {
            "dicom_info": ["exact"],  # Оставляем старый фильтр для одного ID
            "slice_number": ["exact", "in", "gt", "lt"],
        }
