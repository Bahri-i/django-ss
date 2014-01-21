from __future__ import unicode_literals
from decimal import Decimal

from django.test import TestCase
from mock import patch
from prices import Price
from satchless.item import InsufficientStock

from . import Cart, CartPartitioner
from .forms import AddToCartForm, ReplaceCartLineForm, ReplaceCartLineFormSet
from ..product.models import (ProductVariant, StockedProduct, PhysicalProduct,
                              FixedProductDiscount)

__all__ = ['CartTest', 'BigShipCartFormTest']


class BigShip(ProductVariant, StockedProduct, PhysicalProduct):

    pass


class ShipPhoto(ProductVariant):

    pass


class BigShipCartForm(AddToCartForm):

    def get_variant(self, cleaned_data):
        return self.product

stock_product = BigShip(
    stock=10, price=Price(10, currency='USD'), weight=Decimal(123))
stock_product.product = stock_product
digital_product = ShipPhoto(price=Price(10, currency='USD'))
digital_product.product = digital_product


class CartTest(TestCase):

    def test_check_quantity(self):
        'Stock limit works'
        cart = Cart()

        def illegal():
            cart.add(stock_product, 100)

        self.assertRaises(InsufficientStock, illegal)
        self.assertFalse(cart)


class CartPartitionerTest(TestCase):

    def setUp(self):
        self.cart = Cart()

    @patch.object(FixedProductDiscount, 'objects')
    def test_total_price_including_custom_delivery_method(self, mock_manager):
        self.cart.add(stock_product, 1)
        items = CartPartitioner(self.cart)
        self.assertEqual(items.get_total(),
                         Price(10, currency='USD'))


class BigShipCartFormTest(TestCase):

    def setUp(self):
        self.cart = Cart()
        self.post = {'quantity': 5}

    def test_quantity(self):
        'Is BigShipCartForm works with correct quantity value on empty cart'
        form = BigShipCartForm(self.post, cart=self.cart, product=stock_product)
        self.assertTrue(form.is_valid())
        self.assertFalse(self.cart)
        form.save()
        product_quantity = self.cart.get_line(stock_product).quantity
        self.assertEqual(product_quantity, 5, 'Bad quantity')

    def test_max_quantity(self):
        'Is BigShipCartForm works with correct product stock value'
        form = BigShipCartForm(self.post, cart=self.cart, product=stock_product)
        self.assertTrue(form.is_valid())
        form.save()
        form = BigShipCartForm(self.post, cart=self.cart, product=stock_product)
        self.assertTrue(form.is_valid())
        form.save()
        product_quantity = self.cart.get_line(stock_product).quantity
        self.assertEqual(product_quantity, 10,
                         '%s is the bad quantity value' % (product_quantity,))

    def test_too_big_quantity(self):
        'Is BigShipCartForm works with not correct quantity value'
        form = BigShipCartForm({'quantity': 15}, cart=self.cart,
                               product=stock_product)
        self.assertFalse(form.is_valid())
        self.assertFalse(self.cart)

    def test_clean_quantity_product(self):
        'Is BigShipCartForm works with not stocked product'
        cart = Cart()
        self.post['quantity'] = 10000
        form = BigShipCartForm(self.post, cart=cart, product=digital_product)
        self.assertTrue(form.is_valid(), 'Form doesn\'t valitate')
        self.assertFalse(cart, 'Cart isn\'t empty')
        form.save()
        self.assertTrue(cart, 'Cart is empty')


class ReplaceCartLineFormTest(TestCase):

    def setUp(self):
        self.cart = Cart()

    def test_quantity(self):
        'Is ReplaceCartLineForm works with correct quantity value'
        form = ReplaceCartLineForm({'quantity': 5}, cart=self.cart,
                                   product=stock_product)
        self.assertTrue(form.is_valid())
        form.save()
        form = ReplaceCartLineForm({'quantity': 5}, cart=self.cart,
                                   product=stock_product)
        self.assertTrue(form.is_valid())
        form.save()
        product_quantity = self.cart.get_line(stock_product).quantity
        self.assertEqual(product_quantity, 5,
                         '%s is the bad quantity value' % (product_quantity,))

    def test_too_big_quantity(self):
        'Is ReplaceCartLineForm works with to big quantity value'
        form = ReplaceCartLineForm({'quantity': 15}, cart=self.cart,
                                   product=stock_product)
        self.assertFalse(form.is_valid())


class ReplaceCartLineFormSetTest(TestCase):

    def test_save(self):
        post = {
            'form-TOTAL_FORMS': 2,
            'form-INITIAL_FORMS': 2,
            'form-0-quantity': 5,
            'form-1-quantity': 5}
        cart = Cart()
        cart.add(stock_product, 5)
        cart.add(digital_product, 100)
        print 'TETS'
        form = ReplaceCartLineFormSet(post, cart=cart)
        self.assertTrue(form.is_valid())
        form.save()
        product_quantity = cart.get_line(stock_product).quantity
        self.assertEqual(product_quantity, 5,
                         '%s is the bad quantity value' % (product_quantity,))
