# Generated by Django 3.0.10 on 2020-11-05 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=100, null=True)),
                ('header', models.CharField(max_length=50)),
                ('to', models.EmailField(blank=True, max_length=254, null=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('email_from', models.EmailField(default='No Reply <noreply@cjstein.com>', max_length=254)),
                ('html_message', models.TextField()),
                ('template_name', models.CharField(max_length=40)),
            ],
        ),
    ]
