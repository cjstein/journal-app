# Generated by Django 3.0.10 on 2020-12-05 19:36

from django.db import migrations, models

import journal_app.subscription.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_trial',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='trial_end',
            field=models.DateTimeField(default=journal_app.subscription.models.trial_end_date),
        ),
    ]
