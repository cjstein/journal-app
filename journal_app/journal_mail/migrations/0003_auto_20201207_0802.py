# Generated by Django 3.0.10 on 2020-12-07 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal_mail', '0002_mail_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='header',
            field=models.CharField(max_length=100),
        ),
    ]
