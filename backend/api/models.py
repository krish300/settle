from django.db import models


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_ts = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified_ts = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        "ExpenseCategory", on_delete=models.SET_NULL, null=True)
    created_ts = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified_ts = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)


class Bill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        "ExpenseCategory", on_delete=models.SET_NULL, null=True)
    created_ts = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified_ts = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)


class Person(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        "ExpenseCategory", on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    created_ts = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified_ts = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)


class EntryCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_ts = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified_ts = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)


class Entry(models.Model):
    no = models.IntegerField(unique=True)
    product = models.ForeignKey("Product", on_delete=models.PROTECT)
    bill = models.ForeignKey("Bill", on_delete=models.PROTECT)
    person = models.ForeignKey("Person", on_delete=models.PROTECT)
    category = models.ForeignKey(
        "EntryCategory", on_delete=models.PROTECT)
    entry_type = models.CharField(max_length=10)
    mode = models.CharField(max_length=10)
    comment = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(null=False, blank=False)
    created_by = models.CharField(max_length=50)
    last_modified_by = models.CharField(max_length=50)
    created_ts = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified_ts = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = active = models.BooleanField(default=True)
