# Generated by Django 3.0.4 on 2020-03-25 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200322_1444'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesummary',
            name='cash_details',
        ),
        migrations.AddField(
            model_name='settlement',
            name='cash_expense',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='settlement',
            name='closing_cash',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='settlement',
            name='expense',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='settlement',
            name='opening_cash',
            field=models.PositiveIntegerField(default=4000),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CashDetails',
        ),
    ]