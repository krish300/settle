from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import SettlementSerializer

from . import models
from . import serializers


class Base:
    filter_backends = (DjangoFilterBackend,)
    # FIXME(kt): temporaray disable of auth
    #permission_classes = (IsAuthenticated,)


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

    @action(detail=False, methods=['get'], url_path='latest')
    def get_latest(self, request, *args, **kwargs):
        headers = {}
        settlement = SettlementSerializer(models.Settlement.objects.earliest())
        return Response(settlement.data, headers=headers, status=200)


class SaleSummaryViewSet(Base, ModelViewSet):
    queryset = models.SaleSummary.objects.all()
    serializer_class = serializers.SaleSummarySerializer
    filter_fields = ('settlement', 'date')


class PaymentModeViewSet(Base, ReadOnlyModelViewSet):
    queryset = models.PaymentMode.objects.all()
    serializer_class = serializers.PaymentModeSerializer
    filter_fields = ('display_in',)


class AppConfigViewSet(ViewSet):

    def list(self, request, format=None):
        headers = {}
        conf ={}
        app_config = models.AppConfig.objects.all()
        for row in app_config:
            conf[row.prop] = row.value
        return Response(conf, headers=headers, status=200)
