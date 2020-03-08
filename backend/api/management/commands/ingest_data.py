from django.core.management.base import BaseCommand, CommandError
import json
from pathlib import Path
# pylint: disable=import-error
from api.models import EntityType, ExpenseCategory, EntryCategory, Entity


class Command(BaseCommand):
    help = 'Ingest the initial data for models'

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('Started data ingestion...'))
            f_path = f'{Path(__file__).parent.parent.absolute()}\\data\\categories.json'
            with open(f_path) as f:
                data = json.load(f)
                # EntityType
                entity_types = data.get("EntityType")
                entity_types = [EntityType(name=nm) for nm in entity_types]
                print(entity_types)
                EntityType.objects.bulk_create(entity_types)

                # ExpenseCategory
                exp_categories = data.get("ExpenseCategory")
                exp_categories = [ExpenseCategory(
                    name=nm) for nm in exp_categories]
                print(exp_categories)
                ExpenseCategory.objects.bulk_create(exp_categories)

                # EntryCategory
                entry_categories = data.get("EntryCategory")
                entry_categories = [EntryCategory(
                    name=i[0], entity_type=EntityType.objects.get(id=i[1])) for i in entry_categories]
                print(entry_categories)
                EntryCategory.objects.bulk_create(entry_categories)
            f_path = f'{Path(__file__).parent.parent.absolute()}\\data\\data.json'
            with open(f_path) as f:
                data = json.load(f)

                # Entity
                entities = data.get("Entity")
                entities = [Entity(
                    name=i[0], type=EntityType.objects.get(id=i[1]), category=ExpenseCategory.objects.get(id=i[2])) for i in entities]
                print(entities)
                Entity.objects.bulk_create(entities)
        except Exception as e:
            raise CommandError('Error occured', e)

        self.stdout.write(self.style.SUCCESS('Data ingestion complete.'))
