# Generated by Django 3.0.10 on 2020-11-18 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_auto_20201104_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
