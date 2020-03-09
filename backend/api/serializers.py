from rest_framework import serializers
from .models import Entity, EntityType

class EntryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ('name', 'entity_type')

class EntityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityType
        fields = ('name')

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ('name', 'type', 'category')
