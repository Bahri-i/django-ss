# Generated by Django 2.1.5 on 2019-02-25 08:52

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0006_auto_20190220_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='content_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='pagetranslation',
            name='content_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='page',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='pagetranslation',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
