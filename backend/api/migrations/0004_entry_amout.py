# Generated by Django 3.0.4 on 2020-03-17 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200315_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='amout',
            field=models.PositiveIntegerField(default=50),
            preserve_default=False,
        ),
    ]
