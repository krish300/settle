from rest_framework import serializers
from .models import EntryCategory, Entity, EntityType


class EntitySerializer(serializers.ModelSerializer):
    expense_category = serializers.CharField(source='category')

    class Meta:
        model = Entity
        fields = ('name', 'type', 'expense_category', 'category')


class EntityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityType
        fields = ['name']


class EntryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryCategory
        fields = ('name', 'entity_type')


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, max_length=256)
