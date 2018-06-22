# Generated by Django 2.0.3 on 2018-05-29 08:18

from django.db import migrations, models
import django.db.models.deletion
import django_prices.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20180528_1205'),
        ('shipping', '0008_auto_20180108_0814'),
        ('checkout', '0006_auto_20180221_0825'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ('-last_change',)},
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='last_status_change',
            new_name='last_change',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='checkout_data',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='status',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='total',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='voucher',
        ),
        migrations.AddField(
            model_name='cart',
            name='billing_address',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.Address'),
        ),
        migrations.AddField(
            model_name='cart',
            name='discount_amount',
            field=django_prices.models.MoneyField(currency='USD', decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='cart',
            name='discount_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='note',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='cart',
            name='shipping_address',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.Address'),
        ),
        migrations.AddField(
            model_name='cart',
            name='shipping_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carts', to='shipping.ShippingMethodCountry'),
        ),
        migrations.AddField(
            model_name='cart',
            name='voucher_code',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
    ]
