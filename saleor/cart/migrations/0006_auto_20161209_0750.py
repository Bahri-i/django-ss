# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 13:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        # ('product', '0014_auto_20161209_0546'),
        ('cart', '0005_migrate_json_data'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartline',
            unique_together=set([('cart', 'variant', 'data_postgres')]),
        ),
        migrations.RemoveField(
            model_name='cart',
            name='checkout_data',
        ),
        migrations.RemoveField(
            model_name='cartline',
            name='data',
        ),
    ]
