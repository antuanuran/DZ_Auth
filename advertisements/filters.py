from django_filters import rest_framework as filters, DateTimeFromToRangeFilter

from .models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = DateTimeFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['status', 'creator', 'created_at']

