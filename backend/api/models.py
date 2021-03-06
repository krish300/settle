import uuid
from django.db import models


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

    class Meta:
        unique_together = ['name', 'category']

    name = models.CharField(max_length=50)
    type = models.ForeignKey(
        'EntityType', on_delete=models.PROTECT)
    category = models.ForeignKey(
        'ExpenseCategory', on_delete=models.SET_NULL, null=True, blank=True)
    quantity_unit = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class EntryCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    entity_type = models.ForeignKey('EntityType',  on_delete=models.PROTECT)
    expense_category = models.ForeignKey(
        'ExpenseCategory',  on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Entry(models.Model):

    class Meta:
        ordering = ['-date', 'type']

    DEFAULT_ENTRY_TYPE = 'DE'
    ENTRY_TYPE_CHOICES = (
        (DEFAULT_ENTRY_TYPE, 'DEBIT'),
        ('CR', 'CREDIT'),
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
    date = models.DateField()
    mode = models.CharField(
        max_length=2, choices=MODE_CHOICES, default=DEFAULT_MODE)
    comment = models.CharField(max_length=100, blank=True, null=True)
    amount = models.PositiveIntegerField(null=False, blank=False)
    quantity = models.DecimalField(
        null=True, blank=True, max_digits=7, decimal_places=2)
    quantity_unit = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=50, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date}-{self.entity}"


class Settlement(models.Model):
    class Meta:
        ordering = ['-date']
        get_latest_by = '-date'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    date = models.DateField(unique=True)
    opening_cash = models.PositiveIntegerField(null=False, blank=False)
    closing_cash = models.PositiveIntegerField(null=False, blank=False)
    cash_expense = models.PositiveIntegerField(default=0)
    expense = models.PositiveIntegerField(default=0)
    is_closed = models.BooleanField(default=False)
    closed_by = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SaleSummary(models.Model):
    class Meta:
        ordering = ['-date']
        get_latest_by = '-date'
    settlement = models.OneToOneField("Settlement", on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    software_data = models.JSONField(null=True)
    manager_data = models.JSONField(null=True)
    software_sale = models.PositiveIntegerField(null=False, blank=False)
    manager_sale = models.PositiveIntegerField(null=False, blank=False)
    software_discount = models.PositiveIntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"SaleSummary-{self.date}"


class PaymentModeCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PaymentMode(models.Model):
    ENTRY_TYPE_CHOICES = (
        ('MANAGER', 'SaleSummary: ManagerColumn'),
        ('SOFTWARE', 'SaleSummary: SoftwareColumn'),
        ('BOTH', 'SaleSummary: Manager & Software Columns'),
    )
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50, unique=True)
    display_in = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES)
    category = models.ForeignKey(
        "PaymentModeCategory", on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name


class AppConfig(models.Model):
    prop = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    additional_info = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.prop} -> {self.value}"
