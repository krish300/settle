from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Entry, Settlement
from datetime import datetime, timedelta


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


@receiver(post_save, sender=Settlement)
def on_settlement_update(sender, instance, **info):
    # only for updated and NOT created
    if info.get('created') == False:
        # on model close
        if instance.is_closed:
            create_new_settlement()


@receiver(post_delete, sender=Settlement)
def on_settlement_delete(sender, instance, **info):
    create_new_settlement()


def create_new_settlement():
    last_settlement = Settlement.objects.earliest()
    if last_settlement == None:
        opening_cash = 0
        date = datetime.now().strftime('%Y-%m-%d')
    else:
        last_settlement_date = last_settlement.date
        opening_cash = last_settlement.closing_cash
        date = (last_settlement_date + timedelta(days=1)).strftime('%Y-%m-%d')
    name = f'Settlement For Date: {date}'
    settlement = Settlement(
        name=name,
        date=date,
        opening_cash=opening_cash,
        closing_cash=0,
        last_modified_by='Admin:AutoCreate'
    )
    settlement.save()
