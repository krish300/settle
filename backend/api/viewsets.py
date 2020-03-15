from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from . import models
from . import serializers


class EntityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Entity.objects.all()
    serializer_class = serializers.EntitySerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['type', 'category']

class EntityTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.EntityType.objects.all()
    serializer_class = serializers.EntityTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name']


class EntryCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.EntryCategory.objects.all()
    serializer_class = serializers.EntryCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name']


class EntryViewSet(viewsets.ModelViewSet):
    queryset = models.Entry.objects.all()
    serializer_class = serializers.EntrySerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['date', 'settlement']

class SettlementViewSet(viewsets.ModelViewSet):
    queryset = models.Settlement.objects.all()
    serializer_class = serializers.SettlementSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['date', 'name']

class CashDetailsViewSet(viewsets.ModelViewSet):
    queryset = models.CashDetails.objects.all()
    serializer_class = serializers.CashDetailsSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['date']

class SaleSummaryViewSet(viewsets.ModelViewSet):
    queryset = models.SaleSummary.objects.all()
    serializer_class = serializers.SaleSummarySerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['settlement', 'date']

class PaymentModeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.PaymentMode.objects.all()
    serializer_class = serializers.PaymentModeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['display_in']