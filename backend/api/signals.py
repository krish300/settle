from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Entry, Settlement


@receiver([post_save, post_delete], sender=Entry)
def update_settlement(sender, instance, **info):
    settlement = Settlement.objects.get(id=instance.settlement_id)
    # only for debit entry
    if instance.type == 'DE':
        if info.get('created', False):
            if instance.mode == 'CA':
                settlement.cash_expense += instance.amount
            settlement.expense += instance.amount
        else:
            if instance.mode == 'CA':
                settlement.cash_expense -= instance.amount
            settlement.expense -= instance.amount
        settlement.save()
