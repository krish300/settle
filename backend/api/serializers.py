from rest_framework import serializers

from . import models


class EntitySerializer(serializers.ModelSerializer):
    expense_category = serializers.CharField(source='category')

    class Meta:
        model = models.Entity
        fields = ('id', 'name', 'type', 'expense_category', 'category')


class EntityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EntityType
        fields = ('id', 'name')


class EntryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EntryCategory
        fields = ('id', 'name', 'entity_type')


class EntrySerializer(serializers.ModelSerializer):
    expense_category = serializers.CharField(source='category', read_only=True)
    entity_name = serializers.CharField(source='entity', read_only=True)

    class Meta:
        model = models.Entry
        fields = '__all__'
        extra_kwargs = {'date': {'format': '%d-%m-%Y'}}


class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Settlement
        fields = '__all__'
        extra_kwargs = {'date': {'format': '%d-%m-%Y'}}


class CashDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CashDetails
        fields = '__all__'
        extra_kwargs = {'date': {'format': '%d-%m-%Y'}}


class SaleSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SaleSummary
        fields = '__all__'
        extra_kwargs = {'date': {'format': '%d-%m-%Y'}}


class PaymentModeSerializer(serializers.ModelSerializer):
    category_nm = serializers.CharField(source='category', read_only=True)
    class Meta:
        model = models.PaymentMode
        fields = '__all__'


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, max_length=256)
