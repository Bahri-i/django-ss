from typing import Dict, List

import stripe

from ... import TransactionKind
from ...interface import (
    CustomerSource,
    CreditCardInfo,
    GatewayConfig,
    GatewayResponse,
    PaymentData,
)
from .forms import StripePaymentModalForm
from .utils import (
    get_amount_for_stripe,
    get_amount_from_stripe,
    get_currency_for_stripe,
    get_currency_from_stripe,
)


def get_client_token(**_):
    """Not implemented for stripe gateway currently. The client token can be
    generated by Stripe's checkout.js or stripe.js automatically.
    """
    return


def authorize(
    payment_information: PaymentData, config: GatewayConfig
) -> GatewayResponse:
    kind = TransactionKind.CAPTURE if config.auto_capture else TransactionKind.AUTH
    client = _get_client(**config.connection_params)
    currency = get_currency_for_stripe(payment_information.currency)
    stripe_amount = get_amount_for_stripe(payment_information.amount, currency)
    future_use = "off_session" if config.store_customer else "on_session"
    customer_id = PaymentData.customer_id if payment_information.reuse_source else None

    try:
        intent = client.PaymentIntent.create(
            payment_method=payment_information.token,
            amount=stripe_amount,
            currency=currency,
            confirmation_method="manual",
            confirm=True,
            capture_method="automatic" if config.auto_capture else "manual",
            setup_future_usage=future_use,
            customer=customer_id,
        )
        if config.store_customer and not customer_id:
            customer = client.Customer.create(payment_method=intent.payment_method)
            customer_id = customer.id
        response = GatewayResponse(
            is_success=intent.status
            in ("succeeded", "requires_capture", "requires_action"),
            action_required=intent.status == "requires_action",
            transaction_id=intent.id,
            amount=get_amount_from_stripe(intent.amount, currency),
            currency=get_currency_from_stripe(intent.currency),
            error=None,
            kind=kind,
            raw_response=intent,
            customer_id=customer_id,
        )
    except stripe.error.StripeError as exc:
        response = GatewayResponse(
            is_success=False,
            action_required=False,
            transaction_id=payment_information.token,
            amount=payment_information.amount,
            currency=payment_information.currency,
            error=exc.user_message,
            kind=kind,
            raw_response=exc.json_body or {},
            customer_id=customer_id,
        )
    return response


def capture(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    client = _get_client(**config.connection_params)
    intent = None
    try:
        intent = client.PaymentIntent.retrieve(id=payment_information.token)
        capture = intent.capture()
        response = GatewayResponse(
            is_success=capture.status in ("succeeded", "requires_action"),
            action_required=False,
            transaction_id=intent.id,
            amount=get_amount_from_stripe(intent.amount, intent.currency),
            currency=get_currency_from_stripe(intent.currency),
            error=None,
            kind=TransactionKind.CAPTURE,
            raw_response=capture,
        )
    except stripe.error.StripeError as exc:
        action_required = False
        if intent:
            action_required = intent.status == "requires_action"
        response = GatewayResponse(
            is_success=False,
            action_required=action_required,
            transaction_id=payment_information.token,
            amount=payment_information.amount,
            currency=payment_information.currency,
            error=exc.user_message,
            kind=TransactionKind.CAPTURE,
            raw_response=exc.json_body or {},
        )
    return response


def confirm(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    client = _get_client(**config.connection_params)
    try:
        intent = client.PaymentIntent(id=payment_information.token)
        intent.confirm()
        response = GatewayResponse(
            is_success=intent.status in ("succeeded"),
            action_required=False,
            transaction_id=intent.id,
            amount=get_amount_from_stripe(intent.amount, intent.currency),
            currency=get_currency_from_stripe(intent.currency),
            error=None,
            kind=TransactionKind.CAPTURE,
            raw_response=capture,
        )
    except stripe.error.StripeError as exc:
        response = GatewayResponse(
            is_success=False,
            action_required=False,
            transaction_id=payment_information.token,
            amount=payment_information.amount,
            currency=payment_information.currency,
            error=exc.user_message,
            kind=TransactionKind.CAPTURE,
            raw_response=exc.json_body or {},
        )
    return response


def refund(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    client = _get_client(**config.connection_params)
    currency = get_currency_for_stripe(payment_information.currency)
    stripe_amount = get_amount_for_stripe(payment_information.amount, currency)
    try:
        intent = client.PaymentIntent.retrieve(id=payment_information.token)
        refund = intent["charges"]["data"][0].refund(amount=stripe_amount)
        response = GatewayResponse(
            is_success=refund.status == "succeeded",
            action_required=False,
            transaction_id=intent.id,
            amount=payment_information.amount,
            currency=get_currency_from_stripe(refund.currency),
            error=None,
            kind=TransactionKind.REFUND,
            raw_response=refund,
        )
    except stripe.error.StripeError as exc:
        response = GatewayResponse(
            is_success=False,
            action_required=False,
            transaction_id=payment_information.token,
            amount=payment_information.amount,
            currency=payment_information.currency,
            error=exc.user_message,
            kind=TransactionKind.REFUND,
            raw_response=exc.json_body or {},
        )
    return response


def void(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    client = _get_client(**config.connection_params)
    try:
        intent = client.PaymentIntent.retrieve(id=payment_information.token)
        refund = intent["charges"]["data"][0].refund()
        response = GatewayResponse(
            is_success=refund.status == "succeeded",
            action_required=False,
            transaction_id=intent.id,
            amount=get_amount_from_stripe(intent.amount, intent.currency),
            currency=get_currency_from_stripe(refund.currency),
            error=None,
            kind=TransactionKind.VOID,
            raw_response=refund,
        )
    except stripe.error.StripeError as exc:
        response = GatewayResponse(
            is_success=False,
            action_required=False,
            transaction_id=payment_information.token,
            amount=payment_information.amount,
            currency=payment_information.currency,
            error=exc.user_message,
            kind=TransactionKind.VOID,
            raw_response=exc.json_body or {},
        )
    return response


def list_client_sources(
    config: GatewayConfig, customer_id: str
) -> List[CustomerSource]:
    client = _get_client(**config.connection_params)
    cards = client.PaymentMethod.list(customer=customer_id, type="card")["data"]
    return [
        CustomerSource(
            id=c.id,
            gateway="stripe",
            credit_card_info=CreditCardInfo(
                exp_year=c.card.exp_year,
                exp_month=c.card.exp_month,
                last_4=c.card.last4,
                name_on_card=None,
            ),
        )
        for c in cards
    ]


def process_payment(
    payment_information: PaymentData, config: GatewayConfig
) -> GatewayResponse:
    return authorize(payment_information, config)


def create_form(
    data: Dict, payment_information: PaymentData, connection_params: Dict
) -> StripePaymentModalForm:
    return StripePaymentModalForm(
        data=data,
        payment_information=payment_information,
        gateway_params=connection_params,
    )


def _get_client(**connection_params):
    stripe.api_key = connection_params.get("secret_key")
    return stripe
