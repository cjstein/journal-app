# Generated by Django 3.0.10 on 2021-07-01 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal_mail', '0010_auto_20210201_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='email_from',
            field=models.EmailField(default='No Reply<no-reply@cjstein.com>', max_length=254),
        ),
    ]
