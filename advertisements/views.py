from django.conf import settings
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, AdvertisementStatusChoices
from advertisements.permissions import CreatorPermission
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, CreatorPermission]

    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def perform_create(self, serializer):
        status = serializer.validated_data.get('status', AdvertisementStatusChoices.OPEN)

        if status == AdvertisementStatusChoices.OPEN:
            count = Advertisement.objects.filter(status=AdvertisementStatusChoices.OPEN, creator=self.request.user).count()

            if count >= settings.MAX_COUNT_ADVERTISEMENTS:
                raise ValidationError('Превышено количество открытых объялений')

            else:
                serializer.save(creator=self.request.user)

        else:
            serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        status = serializer.validated_data.get('status')

        if status == AdvertisementStatusChoices.OPEN:
            count = Advertisement.objects.filter(status=AdvertisementStatusChoices.OPEN, creator=self.request.user).count()

            if count >= settings.MAX_COUNT_ADVERTISEMENTS:
                raise ValidationError('Превышено количество открытых объялений')

            else:
                serializer.save()

        else:
            serializer.save()

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_anonymous:
            return qs.filter(status=AdvertisementStatusChoices.OPEN)

        else:
            return qs.filter(Q(status=AdvertisementStatusChoices.OPEN) | Q(creator=self.request.user))




