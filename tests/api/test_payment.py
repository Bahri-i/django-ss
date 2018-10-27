import graphene
from tests.api.utils import get_graphql_content

from saleor.payment.models import (
    ChargeStatus, Payment, Transaction, Transactions)
from saleor.graphql.payment.types import (
    PaymentChargeStatusEnum, PaymentGatewayEnum, OrderAction)
from saleor.core.utils import get_country_name_by_code

VOID_QUERY = """
    mutation PaymentVoid($paymentId: ID!) {
        paymentVoid(paymentId: $paymentId) {
            payment {
                id,
                chargeStatus
            }
            errors {
                field
                message
            }
        }
    }
"""


def test_payment_void_success(
        staff_api_client, permission_manage_orders, payment_dummy):
    assert payment_dummy.charge_status == ChargeStatus.NOT_CHARGED
    payment_id = graphene.Node.to_global_id(
        'Payment', payment_dummy.pk)
    variables = {'paymentId': payment_id}
    response = staff_api_client.post_graphql(
        VOID_QUERY, variables, permissions=[permission_manage_orders])
    content = get_graphql_content(response)
    data = content['data']['paymentVoid']
    assert not data['errors']
    payment_dummy.refresh_from_db()
    assert payment_dummy.is_active == False
    assert payment_dummy.transactions.count() == 1
    txn = payment_dummy.transactions.first()
    assert txn.kind == Transactions.VOID


def test_payment_charge_gateway_error(
        staff_api_client, permission_manage_orders, payment_dummy,
        monkeypatch):
    assert payment.charge_status == ChargeStatus.NOT_CHARGED
    payment_id = graphene.Node.to_global_id(
        'Payment', payment_dummy.pk)
    variables = {'paymentId': payment_id}
    monkeypatch.setattr(
        'saleor.payment.gateways.dummy.dummy_success', lambda: False)
    response = staff_api_client.post_graphql(
        VOID_QUERY, variables, permissions=[permission_manage_orders])
    content = get_graphql_content(response)
    data = content['data']['paymentCapture']
    assert data['errors']
    assert data['errors'][0]['field'] is None
    assert data['errors'][0]['message'] == (
        'Only pre-authorized transactions can be void.')
    payment_dummy.refresh_from_db()
    assert payment_dummy.charge_status == ChargeStatus.NOT_CHARGED
    assert payment_dummy.is_active == True
    assert payment_dummy.transactions.count() == 1
    txn = payment_dummy.transactions.first()
    assert txn.kind == Transactions.VOID
    assert not txn.is_success


CREATE_QUERY = """
    mutation CheckoutPaymentCreate($input: PaymentInput!) {
        checkoutPaymentCreate(input: $input) {
            payment {
                transactions {
                    kind,
                    token
                }
                chargeStatus
            }
            errors {
                field
                message
            }
        }
    }
    """


def test_checkout_add_payment(
        user_api_client, cart_with_item, graphql_address_data):
    cart = cart_with_item
    assert cart.user is None

    checkout_id = graphene.Node.to_global_id('Checkout', cart.pk)

    variables = {
        'input': {
            'checkoutId': checkout_id,
            'gateway': 'DUMMY',
            'transactionToken': 'sample-token',
            'amount': str(cart.get_total().gross.amount),
            'billingAddress': graphql_address_data}}
    response = user_api_client.post_graphql(CREATE_QUERY, variables)
    content = get_graphql_content(response)
    data = content['data']['checkoutPaymentCreate']
    assert not data['errors']
    transactions = data['payment']['transactions']
    assert not transactions
    payment = Payment.objects.get()
    assert payment.checkout == cart
    assert payment.is_active
    assert payment.token == 'sample-token'
    total = cart.get_total().gross
    assert payment.total == total.amount
    assert payment.currency == total.currency
    assert payment.charge_status == ChargeStatus.NOT_CHARGED


CHARGE_QUERY = """
    mutation PaymentCharge($paymentId: ID!, $amount: Decimal!) {
        paymentCapture(paymentId: $paymentId, amount: $amount) {
            payment {
                id,
                chargeStatus
            }
            errors {
                field
                message
            }
        }
    }
"""


def test_payment_charge_success(
        staff_api_client, permission_manage_orders, payment_dummy):
    payment = payment_dummy
    assert payment.charge_status == ChargeStatus.NOT_CHARGED
    payment_id = graphene.Node.to_global_id(
        'Payment', payment_dummy.pk)

    variables = {
        'paymentId': payment_id,
        'amount': str(payment_dummy.total)}
    response = staff_api_client.post_graphql(
        CHARGE_QUERY, variables, permissions=[permission_manage_orders])
    content = get_graphql_content(response)
    data = content['data']['paymentCapture']
    assert not data['errors']
    payment_dummy.refresh_from_db()
    assert payment.charge_status == ChargeStatus.CHARGED
    assert payment.transactions.count() == 1
    txn = payment.transactions.first()
    assert txn.kind == Transactions.CHARGE


def test_payment_charge_gateway_error(
        staff_api_client, permission_manage_orders, payment_dummy,
        monkeypatch):
    payment = payment_dummy
    assert payment.charge_status == ChargeStatus.NOT_CHARGED
    payment_id = graphene.Node.to_global_id(
        'Payment', payment_dummy.pk)
    variables = {
        'paymentId': payment_id,
        'amount': str(payment_dummy.total)}
    monkeypatch.setattr(
        'saleor.payment.gateways.dummy.dummy_success', lambda: False)
    response = staff_api_client.post_graphql(
        CHARGE_QUERY, variables, permissions=[permission_manage_orders])
    content = get_graphql_content(response)
    data = content['data']['paymentCapture']
    assert data['errors']
    assert data['errors'][0]['field'] is None
    assert data['errors'][0]['message']

    payment_dummy.refresh_from_db()
    assert payment.charge_status == ChargeStatus.NOT_CHARGED
    assert payment.transactions.count() == 1
    txn = payment.transactions.first()
    assert txn.kind == Transactions.CHARGE
    assert not txn.is_success


REFUND_QUERY = """
    mutation PaymentRefund($paymentId: ID!, $amount: Decimal!) {
        paymentRefund(paymentId: $paymentId, amount: $amount) {
            payment {
                id,
                chargeStatus
            }
            errors {
                field
                message
            }
        }
    }
"""


def test_payment_refund_success(
        staff_api_client, permission_manage_orders, payment_dummy):
    payment = payment_dummy
    payment.charge_status = ChargeStatus.CHARGED
    payment.captured_amount = payment.total
    payment.save()
    payment_id = graphene.Node.to_global_id(
        'Payment', payment.pk)

    variables = {
        'paymentId': payment_id,
        'amount': str(payment_dummy.total)}
    response = staff_api_client.post_graphql(
        REFUND_QUERY, variables, permissions=[permission_manage_orders])
    content = get_graphql_content(response)
    data = content['data']['paymentRefund']
    assert not data['errors']
    payment_dummy.refresh_from_db()
    assert payment.charge_status == ChargeStatus.FULLY_REFUNDED
    assert payment.transactions.count() == 1
    txn = payment.transactions.first()
    assert txn.kind == Transactions.REFUND


def test_payment_refund_error(
        staff_api_client, permission_manage_orders, payment_dummy,
        monkeypatch):
    payment = payment_dummy
    payment.charge_status = ChargeStatus.CHARGED
    payment.captured_amount = payment.total
    payment.save()
    payment_id = graphene.Node.to_global_id(
        'Payment', payment_dummy.pk)
    variables = {
        'paymentId': payment_id,
        'amount': str(payment.total)}
    monkeypatch.setattr(
        'saleor.payment.gateways.dummy.dummy_success', lambda: False)
    response = staff_api_client.post_graphql(
        REFUND_QUERY, variables, permissions=[permission_manage_orders])
    content = get_graphql_content(response)
    data = content['data']['paymentRefund']

    assert data['errors']
    assert data['errors'][0]['field'] is None
    assert data['errors'][0]['message']
    payment_dummy.refresh_from_db()
    assert payment.charge_status == ChargeStatus.CHARGED
    assert payment.transactions.count() == 1
    txn = payment.transactions.first()
    assert txn.kind == Transactions.REFUND
    assert not txn.is_success


def test_payments_query(
        payment_txn_captured, permission_manage_orders, staff_api_client):
    query = """ {
        payments {
            edges {
                node {
                    id
                    gateway
                    capturedAmount {
                        amount
                        currency
                    }
                    total {
                        amount
                        currency
                    }
                    actions
                    chargeStatus
                    billingAddress {
                        country {
                            code
                            country
                        }
                        firstName
                        lastName
                        cityArea
                        countryArea
                        city
                        companyName
                        streetAddress1
                        streetAddress2
                        postalCode
                    }
                    transactions {
                        amount {
                            currency
                            amount
                        }
                    }
                    creditCard {
                        expMonth
                        expYear
                        brand
                        firstDigits
                        lastDigits
                    }
                }
            }
        }
    }
    """
    response = staff_api_client.post_graphql(
        query, permissions=[permission_manage_orders])
    content = get_graphql_content(response)
    data = content['data']['payments']['edges'][0]['node']
    pay = payment_txn_captured
    assert data['gateway'] == pay.gateway
    assert data['capturedAmount'] == {
        'amount': pay.captured_amount, 'currency': pay.currency}
    assert data['total'] == {'amount': pay.total, 'currency': pay.currency}
    assert data['chargeStatus'] == PaymentChargeStatusEnum.CHARGED.name
    assert data['billingAddress'] == {
        'firstName': pay.billing_first_name,
        'lastName': pay.billing_last_name,
        'city': pay.billing_city,
        'cityArea': pay.billing_city_area,
        'countryArea': pay.billing_country_area,
        'companyName': pay.billing_company_name,
        'streetAddress1': pay.billing_address_1,
        'streetAddress2': pay.billing_address_2,
        'postalCode': pay.billing_postal_code,
        'country': {
            'code': pay.billing_country_code,
            'country': get_country_name_by_code(pay.billing_country_code)
        }
    }
    assert data['actions'] == [OrderAction.REFUND.name]
    txn = pay.transactions.get()
    assert data['transactions'] == [{
        'amount': {
            'currency': pay.currency,
            'amount': float(str(txn.amount))}}]
    assert data['creditCard'] == {
        'expMonth': pay.cc_exp_month,
        'expYear': pay.cc_exp_year,
        'brand': pay.cc_brand,
        'firstDigits': pay.cc_first_digits,
        'lastDigits': pay.cc_last_digits}
