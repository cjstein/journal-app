# Generated by Django 3.0.10 on 2020-10-11 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0003_auto_20201008_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='body',
            field=models.TextField(),
        ),
    ]