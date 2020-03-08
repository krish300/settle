from django.db import models

import uuid


class EntityType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Entity(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(
        'EntityType', on_delete=models.PROTECT)
    category = models.ForeignKey(
        'ExpenseCategory', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=50)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class EntryCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    entity_type = models.ForeignKey('EntityType',  on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Entry(models.Model):
    DEFAULT_ENTRY_TYPE = 'CR'
    ENTRY_TYPE_CHOICES = (
        (DEFAULT_ENTRY_TYPE, 'CREDIT'),
        ('DE', 'DEBIT'),
    )
    DEFAULT_MODE = 'CA'
    MODE_CHOICES = (
        (DEFAULT_MODE, 'CASH'),
        ('AC', 'ACCOUNT'),
        ('TR', 'TREASURE')
    )
    settlement = models.ForeignKey("Settlement", on_delete=models.CASCADE)
    entity = models.ForeignKey('Entity', on_delete=models.PROTECT)
    category = models.ForeignKey(
        'EntryCategory', on_delete=models.PROTECT)
    type = models.CharField(
        max_length=2, choices=ENTRY_TYPE_CHOICES, default=DEFAULT_ENTRY_TYPE)
    mode = models.CharField(
        max_length=2, choices=MODE_CHOICES, default=DEFAULT_MODE)
    comment = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=50)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)


class Settlement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=50)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
