# Generated by Django 3.0.10 on 2020-11-03 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal_mail', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='to',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
