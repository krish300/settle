from rest_framework import serializers
from . import models


class EntitySerializer(serializers.ModelSerializer):
    expense_category = serializers.CharField(source='category')

    class Meta:
        model = models.Entity
        fields = ('name', 'type', 'expense_category', 'category')


class EntityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EntityType
        fields = ['name']


class EntryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EntryCategory
        fields = ('name', 'entity_type')

class EntrySerializer(serializers.ModelSerializer):
    expense_category = serializers.CharField(source='category')

    class Meta:
        model = models.Entry
        fields = '__all__'

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Settlement
        fields = '__all__'

class CashDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CashDetails
        fields = '__all__'

class SaleSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SaleSummary
        fields = '__all__'

class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentMode
        fields = '__all__'