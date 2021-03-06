import datetime
from unittest.mock import Mock

import pytest
from prices import Money, TaxedMoney, TaxedMoneyRange

from saleor.extensions.manager import ExtensionsManager
from saleor.product import ProductAvailabilityStatus, VariantAvailabilityStatus, models
from saleor.product.utils.availability import (
    get_product_availability,
    get_product_availability_status,
    get_variant_availability_status,
)


def test_product_availability_status(unavailable_product):
    product = unavailable_product
    product.product_type.has_variants = True

    # product is not published
    status = get_product_availability_status(product)
    assert status == ProductAvailabilityStatus.NOT_PUBLISHED

    product.is_published = True
    product.save()

    # product has no variants
    status = get_product_availability_status(product)
    assert status == ProductAvailabilityStatus.VARIANTS_MISSSING

    variant_1 = product.variants.create(sku="test-1")
    variant_2 = product.variants.create(sku="test-2")

    # create empty stock records
    variant_1.quantity = 0
    variant_2.quantity = 0
    variant_1.save()
    variant_2.save()
    status = get_product_availability_status(product)
    assert status == ProductAvailabilityStatus.OUT_OF_STOCK

    # assign quantity to only one stock record
    variant_1.quantity = 5
    variant_1.save()
    status = get_product_availability_status(product)
    assert status == ProductAvailabilityStatus.LOW_STOCK

    # both stock records have some quantity
    variant_2.quantity = 5
    variant_2.save()
    status = get_product_availability_status(product)
    assert status == ProductAvailabilityStatus.READY_FOR_PURCHASE

    # set product availability date from future
    product.publication_date = datetime.date.today() + datetime.timedelta(days=1)
    product.save()
    status = get_product_availability_status(product)
    assert status == ProductAvailabilityStatus.NOT_YET_AVAILABLE


def test_variant_is_out_of_stock_when_product_is_unavalable(unavailable_product):
    product = unavailable_product
    product.product_type.has_variants = True

    variant = product.variants.create(sku="test")
    variant.quantity = 0
    variant.save(update_fields=["quantity"])

    status = get_variant_availability_status(variant)
    assert status == VariantAvailabilityStatus.OUT_OF_STOCK


@pytest.mark.parametrize(
    "stock, expected_status",
    (
        (0, VariantAvailabilityStatus.OUT_OF_STOCK),
        (1, VariantAvailabilityStatus.AVAILABLE),
    ),
)
def test_variant_availability_status(variant, stock, expected_status):
    variant.quantity = stock
    variant.quantity_allocated = 0

    status = get_variant_availability_status(variant)
    assert status == expected_status


def test_variant_is_still_available_when_another_variant_is_unavailable(
    product_variant_list
):
    """
    Ensure a variant is not incorrectly flagged as out of stock when another variant
    from the parent product is unavailable.
    """

    unavailable_variant, available_variant = product_variant_list[:2]

    unavailable_variant.quantity = 0
    available_variant.quantity = 1
    available_variant.quantity_allocated = 0

    status = get_variant_availability_status(available_variant)
    assert status == VariantAvailabilityStatus.AVAILABLE

    status = get_variant_availability_status(unavailable_variant)
    assert status == VariantAvailabilityStatus.OUT_OF_STOCK


def test_availability(product, monkeypatch, settings):
    taxed_price = TaxedMoney(Money("10.0", "USD"), Money("12.30", "USD"))
    monkeypatch.setattr(
        ExtensionsManager, "apply_taxes_to_product", Mock(return_value=taxed_price)
    )
    availability = get_product_availability(product)
    taxed_price_range = TaxedMoneyRange(start=taxed_price, stop=taxed_price)
    assert availability.price_range == taxed_price_range
    assert availability.price_range_local_currency is None

    monkeypatch.setattr(
        "django_prices_openexchangerates.models.get_rates",
        lambda c: {"PLN": Mock(rate=2)},
    )
    settings.DEFAULT_COUNTRY = "PL"
    settings.OPENEXCHANGERATES_API_KEY = "fake-key"
    availability = get_product_availability(product, local_currency="PLN")
    assert availability.price_range_local_currency.start.currency == "PLN"
    assert availability.available

    availability = get_product_availability(product)
    assert availability.price_range.start.tax.amount
    assert availability.price_range.stop.tax.amount
    assert availability.price_range_undiscounted.start.tax.amount
    assert availability.price_range_undiscounted.stop.tax.amount
    assert availability.available


def test_available_products_only_published(product_list):
    available_products = models.Product.objects.published()
    assert available_products.count() == 2
    assert all([product.is_published for product in available_products])


def test_available_products_only_available(product_list):
    product = product_list[0]
    date_tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    product.publication_date = date_tomorrow
    product.save()
    available_products = models.Product.objects.published()
    assert available_products.count() == 1
    assert all([product.is_visible for product in available_products])
