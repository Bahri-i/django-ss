from datetime import date
from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import pgettext
from django.views.decorators.http import require_POST

from ....discount.models import Voucher
from ..core import load_checkout
from ..forms import CheckoutDiscountForm
from ..utils import recalculate_cart_discount, remove_discount_from_cart


def add_voucher_form(view):
    """Decorate a view injecting a voucher form and handling its submission."""
    @wraps(view)
    def func(request, cart, checkout):
        prefix = 'discount'
        data = {k: v for k, v in request.POST.items() if k.startswith(prefix)}
        voucher_form = CheckoutDiscountForm(
            data or None, checkout=checkout, prefix=prefix, instance=cart)
        if voucher_form.is_bound:
            if voucher_form.is_valid():
                voucher_form.save()
                next_url = request.GET.get(
                    'next', request.META['HTTP_REFERER'])
                return redirect(next_url)
            else:
                remove_discount_from_cart(cart)
                # if only discount form was used we clear post for other forms
                request.POST = {}
        else:
            recalculate_cart_discount(cart, checkout)
        response = view(request, cart, checkout)
        if isinstance(response, TemplateResponse):
            voucher = voucher_form.initial.get('voucher')
            response.context_data['voucher_form'] = voucher_form
            response.context_data['voucher'] = voucher
        return response
    return func


def validate_voucher(view):
    """Decorate a view making it check whether a discount voucher is valid.

    If the voucher is invalid it will be removed and the user will be
    redirected to the checkout summary view.
    """
    @wraps(view)
    def func(request, cart, checkout):
        if cart.voucher_code:
            try:
                Voucher.objects.active(date=date.today()).get(
                    code=cart.voucher_code)
            except Voucher.DoesNotExist:
                cart.voucher_code = ''
                cart.save()
                recalculate_cart_discount(cart, checkout)
                msg = pgettext(
                    'Checkout warning',
                    'This voucher has expired. Please review your checkout.')
                messages.warning(request, msg)
                return redirect('cart:checkout-summary')
        return view(request, cart, checkout)
    return func


@require_POST
@load_checkout
def remove_voucher_view(request, cart, checkout):
    """Clear the discount and remove the voucher."""
    next_url = request.GET.get('next', request.META['HTTP_REFERER'])
    remove_discount_from_cart(cart)
    return redirect(next_url)
