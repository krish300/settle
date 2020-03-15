import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

# pylint: disable=import-error
from api.models import EntityType, ExpenseCategory, EntryCategory, Entity, PaymentModeCategory, PaymentMode


class Command(BaseCommand):
    help = 'Ingest the initial data for models'

    def success(self, s):
        self.stdout.write(self.style.SUCCESS(s))

    def handle(self, *args, **options):
        try:
            self.success('Started data ingestion...')
            data_file = f'{Path(__file__).parent.parent.absolute()}/data/data.json'

            with open(data_file) as f:
                data = json.load(f)

                self.success('Ingesting: EntityType')
                entity_types = data.get('EntityType')
                entity_type_objs = [EntityType(name=i) for i in entity_types]
                EntityType.objects.bulk_create(entity_type_objs)

                self.success('Ingesting: ExpenseCategory')
                exp_categories = data.get('ExpenseCategory')
                exp_category_objs = [ExpenseCategory(name=i) for i in exp_categories]
                ExpenseCategory.objects.bulk_create(exp_category_objs)

                self.success('Ingesting: EntryCategory')
                entry_categories = data.get('EntryCategory')
                entry_category_objs = [
                    EntryCategory(
                        name=i[0],
                        entity_type=EntityType.objects.get(id=i[1])
                    ) for i in entry_categories
                ]
                EntryCategory.objects.bulk_create(entry_category_objs)

                self.success('Ingesting: Entity')
                entities = data.get('Entity')
                entity_objs = [
                    Entity(
                        name=i[0],
                        type=EntityType.objects.get(id=i[1]),
                        category=ExpenseCategory.objects.get(id=i[2])
                    ) for i in entities
                ]
                Entity.objects.bulk_create(entity_objs)

                self.success('Ingesting: PaymentModeCategory')
                pay_categories = data.get('PaymentModeCategory')
                pay_category_objs = [PaymentModeCategory(name=i) for i in pay_categories]
                PaymentModeCategory.objects.bulk_create(pay_category_objs)

                self.success('Ingesting: PaymentMode')
                payment_modes = data.get('PaymentMode')
                payment_mode_objs = []
                for i in payment_modes:
                    cat=None
                    if i[2] != None:
                        cat=PaymentModeCategory.objects.get(name=i[2])
                    payment_mode_objs.append(PaymentMode(name=i[0],display_in=i[1], category=cat))
                PaymentMode.objects.bulk_create(payment_mode_objs)

        except Exception as e:
            raise CommandError('Error occured', e)

        self.success('Data ingestion complete.')
