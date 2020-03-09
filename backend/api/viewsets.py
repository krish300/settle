from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Entity, EntityType, EntryCategory
from .serializers import EntitySerializer, EntityTypeSerializer, EntryCategorySerializer


class EntityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['type', 'category']

class EntityTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EntityType.objects.all()
    serializer_class = EntityTypeSerializer


class EntryCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EntryCategory.objects.all()
    serializer_class = EntryCategorySerializer
