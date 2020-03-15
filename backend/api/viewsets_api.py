from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from . import models
from . import serializers


class Base:
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)


class EntityViewSet(Base, ReadOnlyModelViewSet):
    queryset = models.Entity.objects.all()
    serializer_class = serializers.EntitySerializer
    filter_fields = ('type', 'category')


class EntityTypeViewSet(Base, ReadOnlyModelViewSet):
    queryset = models.EntityType.objects.all()
    serializer_class = serializers.EntityTypeSerializer
    filter_fields = ('name',)


class EntryCategoryViewSet(Base, ReadOnlyModelViewSet):
    queryset = models.EntryCategory.objects.all()
    serializer_class = serializers.EntryCategorySerializer
    filter_fields = ('name',)


class EntryViewSet(Base, ModelViewSet):
    queryset = models.Entry.objects.all()
    serializer_class = serializers.EntrySerializer
    filter_fields = ('date', 'settlement')


class SettlementViewSet(Base, ModelViewSet):
    queryset = models.Settlement.objects.all()
    serializer_class = serializers.SettlementSerializer
    filter_fields = ('date', 'name')


class CashDetailsViewSet(Base, ModelViewSet):
    queryset = models.CashDetails.objects.all()
    serializer_class = serializers.CashDetailsSerializer
    filter_fields = ('date',)


class SaleSummaryViewSet(Base, ModelViewSet):
    queryset = models.SaleSummary.objects.all()
    serializer_class = serializers.SaleSummarySerializer
    filter_fields = ('settlement', 'date')


class PaymentModeViewSet(Base, ReadOnlyModelViewSet):
    queryset = models.PaymentMode.objects.all()
    serializer_class = serializers.PaymentModeSerializer
    filter_fields = ('display_in',)
