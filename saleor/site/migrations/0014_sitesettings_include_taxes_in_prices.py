# Generated by Django 2.0.3 on 2018-04-16 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0013_assign_default_menus'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='include_taxes_in_prices',
            field=models.BooleanField(default=True),
        ),
    ]
