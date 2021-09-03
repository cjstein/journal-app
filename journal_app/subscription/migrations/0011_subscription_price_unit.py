# Generated by Django 3.0.10 on 2021-08-17 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0010_auto_20210816_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='price_unit',
            field=models.CharField(choices=[('monthly', '/ month'), ('yearly', '/ year'), ('lifetime', 'forever')], default='monthly', max_length=10),
        ),
    ]