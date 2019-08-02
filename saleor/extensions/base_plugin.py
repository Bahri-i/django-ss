from decimal import Decimal
from typing import TYPE_CHECKING, Any, List, Union

from django.db.models import QuerySet
from django_countries.fields import Country
from prices import Money, MoneyRange, TaxedMoney, TaxedMoneyRange

if TYPE_CHECKING:
    from ..core.taxes import TaxType
    from ..checkout.models import Checkout, CheckoutLine
    from ..product.models import Product
    from ..account.models import Address
    from ..order.models import OrderLine, Order
    from .models import PluginConfiguration


class BasePlugin:
    """Abstract class for storing all methods available for any plugin.

    All methods take previous_value parameter.
    previous_value contains a value calculated by the previous plugin in the queue.
    If the plugin is first, it will use default value calculated by the manager.
    """

    PLUGIN_NAME = ""

    def __str__(self):
        return self.PLUGIN_NAME

    def calculate_checkout_total(
        self,
        checkout: "Checkout",
        discounts: List["DiscountInfo"],
        previous_value: TaxedMoney,
    ) -> TaxedMoney:
        return NotImplemented

    def calculate_checkout_subtotal(
        self,
        checkout: "Checkout",
        discounts: List["DiscountInfo"],
        previous_value: TaxedMoney,
    ) -> TaxedMoney:
        return NotImplemented

    def calculate_checkout_shipping(
        self,
        checkout: "Checkout",
        discounts: List["DiscountInfo"],
        previous_value: TaxedMoney,
    ) -> TaxedMoney:
        return NotImplemented

    def calculate_order_shipping(
        self, order: "Order", previous_value: TaxedMoney
    ) -> TaxedMoney:
        return NotImplemented

    def calculate_checkout_line_total(
        self,
        checkout_line: "CheckoutLine",
        discounts: List["DiscountInfo"],
        previous_value: TaxedMoney,
    ) -> TaxedMoney:
        return NotImplemented

    def calculate_order_line_unit(
        self, order_line: "OrderLine", previous_value: TaxedMoney
    ) -> TaxedMoney:
        return NotImplemented

    def get_tax_rate_type_choices(
        self, previous_value: List["TaxType"]
    ) -> List["TaxType"]:
        return NotImplemented

    def show_taxes_on_storefront(self, previous_value: bool) -> bool:
        return NotImplemented

    def taxes_are_enabled(self, previous_value: bool) -> bool:
        return NotImplemented

    def apply_taxes_to_shipping_price_range(
        self, prices: MoneyRange, country: Country, previous_value: TaxedMoneyRange
    ) -> TaxedMoneyRange:
        return NotImplemented

    def apply_taxes_to_shipping(
        self, price: Money, shipping_address: "Address", previous_value: TaxedMoney
    ) -> TaxedMoney:
        return NotImplemented

    def apply_taxes_to_product(
        self,
        product: "Product",
        price: Money,
        country: Country,
        previous_value: TaxedMoney,
    ) -> TaxedMoney:
        return NotImplemented

    def preprocess_order_creation(
        self, checkout: "Checkout", discounts: List["DiscountInfo"], previous_value: Any
    ):
        return NotImplemented

    def postprocess_order_creation(self, order: "Order", previous_value: Any):
        return NotImplemented

    def assign_tax_code_to_object_meta(
        self, obj: Union["Product", "ProductType"], tax_code: str, previous_value: Any
    ):
        return NotImplemented

    def get_tax_code_from_object_meta(
        self, obj: Union["Product", "ProductType"], previous_value: "TaxType"
    ) -> "TaxType":
        return NotImplemented

    def get_tax_rate_percentage_value(
        self, obj: Union["Product", "ProductType"], country: Country, previous_value
    ) -> Decimal:
        return NotImplemented

    @classmethod
    def _update_config_items(cls, configuration_to_update: dict, current_config: dict):
        for config_item in current_config:
            for config_item_to_update in configuration_to_update:
                if config_item["name"] == config_item_to_update.get("name"):
                    new_value = config_item_to_update.get("value")
                    config_item.update([("value", new_value)])

    @classmethod
    def save_plugin_configuration(
        cls, plugin_configuration: "PluginConfiguration", cleaned_data
    ):
        current_config = plugin_configuration.configuration
        configuration_to_update = cleaned_data.get("configuration")
        if configuration_to_update:
            cls._update_config_items(configuration_to_update, current_config)
        if "active" in cleaned_data:
            plugin_configuration.active = cleaned_data["active"]
        plugin_configuration.save()
        return plugin_configuration

    @classmethod
    def _get_default_configuration(cls):
        defaults = None
        return defaults

    @classmethod
    def get_plugin_configuration(cls, queryset: QuerySet) -> "PluginConfiguration":
        defaults = cls._get_default_configuration()
        configuration = queryset.get_or_create(name=cls.PLUGIN_NAME, defaults=defaults)[
            0
        ]
        return configuration
