from __future__ import unicode_literals

import uuid
import pytest
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from mock import Mock

from saleor.cart import decorators
from saleor.cart.decorators import get_or_empty_db_cart, get_cart_from_request
from saleor.cart.models import Cart


def get_request(django_user_model, cookie_token, authenticated=True):
    if authenticated:
        user = django_user_model.objects.get_or_create(
            email='admin@example.com', defaults={'is_active': True})[0]
    else:
        user = AnonymousUser()

    return Mock(user=user, get_signed_cookie=lambda name, default: cookie_token)


def test_get_cart_from_request_anonymous(monkeypatch):
    request = Mock(user=AnonymousUser(), discounts=[])
    empty_cart = Cart()
    qs_mock = Mock(return_value=[empty_cart])
    qs_mock.get.return_value = empty_cart
    qs_mock.open.return_value = qs_mock
    qs_mock.filter.return_value = qs_mock
    cart = decorators.get_cart_from_request(request, cart_queryset=qs_mock)
    assert cart.pk == empty_cart.pk


def test_get_cart_from_request_authenticated(django_user_model):
    token = Cart().token
    request = get_request(django_user_model, authenticated=True,
                          cookie_token=token)
    cart = Cart.objects.create(user=request.user, status=Cart.OPEN, token=token)
    user_cart = decorators.get_cart_from_request(request)
    assert cart.token == user_cart.token


@pytest.mark.integration
def test_get_cart_from_request_authenticated_no_cart(django_user_model):
    user = django_user_model.objects.get_or_create(
        email='user@example.com', defaults={'is_active': True})[0]
    anonymous_token = uuid.uuid4()
    Cart.objects.create(status=Cart.OPEN, token=anonymous_token, user=None)
    request = Mock(spec=HttpRequest, discounts=[], user=user,
                   get_signed_cookie=Mock(return_value=anonymous_token))
    cart = get_cart_from_request(request, create=True)
    assert cart.token != anonymous_token


def test_get_or_create_db_cart(monkeypatch, django_user_model):
    empty_cart = Cart()
    request = get_request(django_user_model, authenticated=True,
                          cookie_token=empty_cart.token)
    monkeypatch.setattr(decorators, 'get_cart_from_request',
                        lambda r, cart_queryset, create: empty_cart)
    decorated_view = decorators.get_or_create_db_cart()(lambda r, c: c)
    response_cart = decorated_view(request)
    assert response_cart.token == empty_cart.token


def test_find_and_assign_cart(django_user_model):
    cart = Cart.objects.create(user=None, status=Cart.OPEN)
    request = get_request(django_user_model, authenticated=True,
                          cookie_token=cart.token)
    decorators.find_and_assign_cart(request, response=Mock())
    cart = Cart.objects.get(token=cart.token)
    assert cart.user == request.user


@pytest.mark.parametrize('token', [Cart().token, None])
def test_find_and_assign_cart_cart_missing(token, django_user_model):
    request = get_request(django_user_model, authenticated=True,
                          cookie_token=token)
    decorators.find_and_assign_cart(request, response=Mock())
    assert Cart.objects.filter(user=request.user).exists() is False


def test_get_or_empty_db_cart(rf, monkeypatch):
    request = rf.get('/')
    empty_cart = Cart()
    monkeypatch.setattr(decorators, 'get_cart_from_request',
                        lambda req, cart_queryset: empty_cart)
    decorated_view = get_or_empty_db_cart()(lambda req, cart: cart)
    view_cart = decorated_view(request)
    assert view_cart.pk == empty_cart.pk


@pytest.mark.parametrize('authenticated, method_called', [
    (True, True),
    (False, False)])
def test_assign_anonymous_cart(authenticated, method_called,
                               django_user_model, monkeypatch):
    token = Cart().token
    request = get_request(django_user_model, authenticated=authenticated,
                          cookie_token=token)
    find_and_assign = Mock()
    monkeypatch.setattr(decorators, 'find_and_assign_cart', find_and_assign)
    decorated_view = decorators.assign_anonymous_cart(lambda req: Mock())
    decorated_view(request)
    assert find_and_assign.called is method_called
