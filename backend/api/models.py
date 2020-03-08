from django.db import models


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_active = models.BooleanField(default=True)


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        'ExpenseCategory', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_active = models.BooleanField(default=True)


class Bill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        'ExpenseCategory', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_active = models.BooleanField(default=True)


class EntryCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_active = models.BooleanField(default=True)


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
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    bill = models.ForeignKey('Bill', on_delete=models.PROTECT)
    person = models.ForeignKey('Person', on_delete=models.PROTECT)
    category = models.ForeignKey(
        'EntryCategory', on_delete=models.PROTECT)
    type = models.CharField(
        max_length=2, choices=ENTRY_TYPE_CHOICES, default=DEFAULT_ENTRY_TYPE)
    mode = models.CharField(
        max_length=2, choices=MODE_CHOICES, default=DEFAULT_MODE)
    comment = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.CharField(max_length=50)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    last_modified_by = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
