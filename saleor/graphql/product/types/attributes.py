import re

import graphene
import graphene_django_optimizer as gql_optimizer
from graphene import relay
from graphql_jwt.decorators import permission_required

from ....product import models
from ...core.connection import CountableDjangoObjectType
from ...core.resolvers import resolve_meta, resolve_private_meta
from ...core.types import MetadataObjectType
from ...translations.enums import LanguageCodeEnum
from ...translations.resolvers import resolve_translation
from ...translations.types import AttributeTranslation, AttributeValueTranslation
from ..descriptions import AttributeDescriptions, AttributeValueDescriptions
from ..enums import (
    AttributeInputTypeEnum,
    AttributeSortField,
    AttributeValueType,
    OrderDirection,
)

COLOR_PATTERN = r"^(#[0-9a-fA-F]{3}|#(?:[0-9a-fA-F]{2}){2,4}|(rgb|hsl)a?\((-?\d+%?[,\s]+){2,3}\s*[\d\.]+%?\))$"  # noqa
color_pattern = re.compile(COLOR_PATTERN)


def resolve_attribute_value_type(attribute_value):
    if color_pattern.match(attribute_value):
        return AttributeValueType.COLOR
    if "gradient(" in attribute_value:
        return AttributeValueType.GRADIENT
    if "://" in attribute_value:
        return AttributeValueType.URL
    return AttributeValueType.STRING


class AttributeSortingInput(graphene.InputObjectType):
    field = graphene.Argument(
        AttributeSortField,
        required=True,
        description="Sort attributes by the selected field.",
    )
    direction = graphene.Argument(
        OrderDirection,
        required=True,
        description="Specifies the direction in which to sort the attributes",
    )


class AttributeValue(CountableDjangoObjectType):
    name = graphene.String(description=AttributeValueDescriptions.NAME)
    slug = graphene.String(description=AttributeValueDescriptions.SLUG)
    type = AttributeValueType(description=AttributeValueDescriptions.TYPE)
    value = graphene.String(description=AttributeValueDescriptions.VALUE)
    translation = graphene.Field(
        AttributeValueTranslation,
        language_code=graphene.Argument(
            LanguageCodeEnum,
            description="A language code to return the translation for.",
            required=True,
        ),
        description=(
            "Returns translated Attribute Value fields " "for the given language code."
        ),
        resolver=resolve_translation,
    )

    input_type = gql_optimizer.field(
        AttributeInputTypeEnum(description=AttributeDescriptions.INPUT_TYPE),
        model_field="attribute",
    )

    class Meta:
        description = "Represents a value of an attribute."
        only_fields = ["id", "sort_order"]
        interfaces = [relay.Node]
        model = models.AttributeValue

    @staticmethod
    def resolve_type(root: models.AttributeValue, *_args):
        return resolve_attribute_value_type(root.value)

    @staticmethod
    @permission_required("product.manage_products")
    def resolve_input_type(root: models.AttributeValue, *_args):
        return root.input_type


class Attribute(CountableDjangoObjectType, MetadataObjectType):
    input_type = AttributeInputTypeEnum(description=AttributeDescriptions.INPUT_TYPE)

    name = graphene.String(description=AttributeDescriptions.NAME)
    slug = graphene.String(description=AttributeDescriptions.SLUG)

    values = gql_optimizer.field(
        graphene.List(AttributeValue, description=AttributeDescriptions.VALUES),
        model_field="values",
    )

    value_required = gql_optimizer.field(
        graphene.Boolean(description=AttributeDescriptions.VALUE_REQUIRED),
        model_field="value_required",
    )

    visible_in_storefront = gql_optimizer.field(
        graphene.Boolean(description=AttributeDescriptions.VISIBLE_IN_STOREFRONT),
        model_field="visible_in_storefront",
    )

    filterable_in_storefront = gql_optimizer.field(
        graphene.Boolean(description=AttributeDescriptions.FILTERABLE_IN_STOREFRONT),
        model_field="filterable_in_storefront",
    )
    filterable_in_dashboard = gql_optimizer.field(
        graphene.Boolean(description=AttributeDescriptions.FILTERABLE_IN_DASHBOARD),
        model_field="filterable_in_dashboard",
    )

    translation = graphene.Field(
        AttributeTranslation,
        language_code=graphene.Argument(
            LanguageCodeEnum,
            description="A language code to return the translation for.",
            required=True,
        ),
        description=(
            "Returns translated Attribute fields " "for the given language code."
        ),
        resolver=resolve_translation,
    )

    storefront_search_position = gql_optimizer.field(
        graphene.Int(description=AttributeDescriptions.STOREFRONT_SEARCH_POSITION),
        model_field="storefront_search_position",
    )

    class Meta:
        description = """
            Custom attribute of a product. Attributes can be
            assigned to products and variants at the product type level."""
        only_fields = ["id", "product_types", "product_variant_types"]
        interfaces = [relay.Node]
        model = models.Attribute

    @staticmethod
    def resolve_values(root: models.Attribute, *_args):
        return root.values.all()

    @staticmethod
    @permission_required("product.manage_products")
    def resolve_private_meta(root, _info):
        return resolve_private_meta(root, _info)

    @staticmethod
    def resolve_meta(root, _info):
        return resolve_meta(root, _info)

    @staticmethod
    @permission_required("product.manage_products")
    def resolve_value_required(root: models.Attribute, *_args):
        return root.value_required

    @staticmethod
    @permission_required("product.manage_products")
    def resolve_visible_in_storefront(root: models.Attribute, *_args):
        return root.visible_in_storefront

    @staticmethod
    @permission_required("product.manage_products")
    def resolve_filterable_in_storefront(root: models.Attribute, *_args):
        return root.filterable_in_storefront

    @staticmethod
    @permission_required("product.manage_products")
    def resolve_filterable_in_dashboard(root: models.Attribute, *_args):
        return root.filterable_in_dashboard

    @staticmethod
    @permission_required("product.manage_products")
    def resolve_storefront_search_position(root: models.Attribute, *_args):
        return root.storefront_search_position


class SelectedAttribute(graphene.ObjectType):
    attribute = graphene.Field(
        Attribute,
        default_value=None,
        description=AttributeDescriptions.NAME,
        required=True,
    )
    value = graphene.Field(
        AttributeValue,
        default_value=None,
        description="The value or the first value of an attribute.",
        deprecation_reason="Use values instead.",
    )
    values = graphene.List(
        AttributeValue, description="Values of an attribute.", required=True
    )

    class Meta:
        description = "Represents a custom attribute."


class AttributeInput(graphene.InputObjectType):
    slug = graphene.String(required=True, description=AttributeDescriptions.SLUG)
    value = graphene.String(required=True, description=AttributeValueDescriptions.SLUG)
