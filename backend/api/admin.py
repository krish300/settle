from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from . import models


# https://realpython.com/manage-users-in-django-admin/
# Unregister the provided model admin
admin.site.unregister(User)

# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = [
        'date_joined',
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions'
            }

        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


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

@admin.register(models.SaleSummary)
class SaleSummary(admin.ModelAdmin):
    pass

@admin.register(models.PaymentModeCategory)
class PaymentModeCategory(admin.ModelAdmin):
    pass

@admin.register(models.PaymentMode)
class PaymentMode(admin.ModelAdmin):
    pass

@admin.register(models.AppConfig)
class AppConfig(admin.ModelAdmin):
    pass

@admin.register(models.Entry)
class Entry(admin.ModelAdmin):
    pass
