from textwrap import dedent

import graphene
from django.conf import settings
from django.core.exceptions import ValidationError
from graphql_jwt.decorators import permission_required

from ...core.utils import get_client_ip
from ...core.utils.taxes import get_taxes_for_address
from ...payment import PaymentError
from ...payment.utils import (
    create_payment, gateway_capture, gateway_refund, gateway_void)
from ..account.i18n import I18nMixin
from ..account.types import AddressInput
from ..checkout.types import Checkout
from ..core.mutations import BaseMutation
from ..core.scalars import Decimal
from .enums import PaymentGatewayEnum
from .types import Payment


class PaymentInput(graphene.InputObjectType):
    gateway = graphene.Field(
        PaymentGatewayEnum, description='A gateway to use with that payment.',
        required=True)
    token = graphene.String(
        required=True,
        description=(
            'Client-side generated payment token, representing customer\'s '
            'billing data in a secure manner.'))
    amount = Decimal(
        required=False,
        description=(
            'Total amount of the transaction, including '
            'all taxes and discounts. If no amount is provided, '
            'the checkout total will be used.'))
    billing_address = AddressInput(
        description=dedent(
            '''Billing address. If empty, the billing address associated with
            the checkout instance will be used.'''))


class CheckoutPaymentCreate(BaseMutation, I18nMixin):
    checkout = graphene.Field(Checkout, description='Related checkout object.')
    payment = graphene.Field(Payment, description='A newly created payment.')

    class Arguments:
        checkout_id = graphene.ID(description='Checkout ID.', required=True)
        input = PaymentInput(
            description='Data required to create a new payment.',
            required=True)

    class Meta:
        description = 'Create a new payment for given checkout.'

    @classmethod
    def perform_mutation(cls, root, info, checkout_id, input):
        errors = []
        checkout = cls.get_node_or_error(
            info, checkout_id, errors, 'checkout_id', only_type=Checkout)

        billing_address = checkout.billing_address
        if 'billing_address' in input:
            billing_address = cls.validate_address(input['billing_address'])
        if billing_address is None:
            raise ValidationError({
                'billing_address':
                'No billing address associated with this checkout.'})

        checkout_total = checkout.get_total(
            discounts=info.context.discounts,
            taxes=get_taxes_for_address(checkout.billing_address))
        amount = input.get('amount', checkout_total)
        if amount < checkout_total.gross.amount:
            raise ValidationError({
                'amount':
                'Partial payments are not allowed, amount should be '
                'equal checkout\'s total.'})

        extra_data = {
            'customer_user_agent': info.context.META.get('HTTP_USER_AGENT')}

        payment = create_payment(
            gateway=input['gateway'],
            payment_token=input['token'],
            total=amount,
            currency=settings.DEFAULT_CURRENCY,
            email=checkout.email,
            billing_address=billing_address,
            extra_data=extra_data,
            customer_ip_address=get_client_ip(info.context),
            checkout=checkout)
        return CheckoutPaymentCreate(payment=payment)


class PaymentCapture(BaseMutation):
    payment = graphene.Field(Payment, description='Updated payment')

    class Arguments:
        payment_id = graphene.ID(required=True, description='Payment ID')
        amount = Decimal(description='Transaction amount')

    class Meta:
        description = 'Captures the authorized payment amount'

    @classmethod
    def user_is_allowed(cls, user, input):
        return user.has_perm('order.manage_orders')

    @classmethod
    def perform_mutation(cls, root, info, payment_id, amount=None):
        errors = []
        payment = cls.get_node_or_error(
            info, payment_id, errors, 'payment_id', only_type=Payment)

        try:
            gateway_capture(payment, amount)
        except PaymentError as e:
            raise ValidationError(str(e))
        return PaymentCapture(payment=payment)


class PaymentRefund(PaymentCapture):

    class Meta:
        description = 'Refunds the captured payment amount'

    @classmethod
    def user_is_allowed(cls, user, input):
        return user.has_perm('order.manage_orders')

    @classmethod
    def perform_mutation(cls, root, info, payment_id, amount=None):
        errors = []
        payment = cls.get_node_or_error(
            info, payment_id, errors, 'payment_id', only_type=Payment)

        try:
            gateway_refund(payment, amount=amount)
        except PaymentError as e:
            raise ValidationError(str(e))
        return PaymentRefund(payment=payment)


class PaymentVoid(BaseMutation):
    payment = graphene.Field(Payment, description='Updated payment')

    class Arguments:
        payment_id = graphene.ID(required=True, description='Payment ID')

    class Meta:
        description = 'Voids the authorized payment'

    @classmethod
    def user_is_allowed(cls, user, input):
        return user.has_perm('order.manage_orders')

    @classmethod
    def perform_mutation(cls, root, info, payment_id, amount=None):
        errors = []
        payment = cls.get_node_or_error(
            info, payment_id, errors, 'payment_id', only_type=Payment)

        try:
            gateway_void(payment)
        except PaymentError as e:
            raise ValidationError(str(e))
        return PaymentVoid(payment=payment)
