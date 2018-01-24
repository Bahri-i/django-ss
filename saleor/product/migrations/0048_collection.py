# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-24 10:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0047_auto_20180117_0359'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField()),
                ('products', models.ManyToManyField(blank=True, related_name='collections', to='product.Product')),
            ],
        ),
    ]
