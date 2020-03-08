from django.db import models


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=True)


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        "ExpenseCategory", on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)
