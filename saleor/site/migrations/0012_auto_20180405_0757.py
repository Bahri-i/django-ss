# Generated by Django 2.0.3 on 2018-04-05 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0002_auto_20180319_0412"),
        ("site", "0011_auto_20180108_0814"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="bottom_menu",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="menu.Menu",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="top_menu",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="menu.Menu",
            ),
        ),
    ]
