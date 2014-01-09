from __future__ import unicode_literals
from re import sub

from django.conf import settings
from prices import Price
from satchless.item import ItemSet

from ..cart import ShippedGroup


class BaseDelivery(ItemSet):

    group = None

    def __init__(self, delivery_group):
        self.group = delivery_group

    def __iter__(self):
        return iter(self.group)

    def get_delivery_total(self, **kwargs):
        return Price(0, currency=settings.SATCHLESS_DEFAULT_CURRENCY)

    def get_total_with_delivery(self):
        return self.group.get_total() + self.get_delivery_total()

    @property
    def name(self):
        '''
        Returns undescored version of class name
        '''
        name = type(self).__name__
        name = sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', name)
        return name.lower().strip('_')


class DummyShipping(BaseDelivery):

    address = None

    def __init__(self, delivery_group, address):
        self.address = address
        super(DummyShipping, self).__init__(delivery_group)

    def __unicode__(self):
        return 'Dummy shipping'

    def get_delivery_total(self, **kwargs):
        weight = sum(line.product.weight for line in self.group)
        qty = sum(line.quantity for line in self.group)
        return Price(qty * weight,
                     currency=settings.SATCHLESS_DEFAULT_CURRENCY)


class DigitalDelivery(BaseDelivery):

    email = None

    def __init__(self, delivery_group, email):
        self.email = email
        super(DigitalDelivery, self).__init__(delivery_group)

    def __unicode__(self):
        return 'Digital delivery'


def get_delivery_methods_for_group(group, **kwargs):
    if isinstance(group, ShippedGroup):
        yield DummyShipping(group, kwargs['address'])
    else:
        yield DigitalDelivery(group, kwargs['email'])
