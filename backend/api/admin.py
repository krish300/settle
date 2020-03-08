from django.contrib import admin

from . import models


@admin.register(models.EntityType)
class EntityTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Entity)
class EntityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EntryCategory)
class EntryCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Settlement)
class SettlementAdmin(admin.ModelAdmin):
    pass
