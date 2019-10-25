from typing import List

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import pgettext_lazy

from ...extensions.manager import get_extensions_manager
from ..views import staff_member_required
from .forms import GatewayConfigurationForm


def list_payments_plugins(active_only: bool = False) -> List[str]:
    payment_method = "process_payment"
    extension_manager = get_extensions_manager()
    plugins = extension_manager.plugins
    if active_only:
        plugins = extension_manager.get_active_plugins()
    return [
        plugin.PLUGIN_NAME
        for plugin in plugins
        if payment_method in type(plugin).__dict__
    ]


@staff_member_required
@permission_required("extensions.manage_plugins")
def index(request: "HttpRequest") -> TemplateResponse:
    ctx = {"payment_gateways": list_payments_plugins()}
    return TemplateResponse(request, "dashboard/payments/index.html", ctx)


@staff_member_required
@permission_required("extensions.manage_plugins")
def configure_payment_gateway(request: HttpRequest, plugin_name: str) -> HttpResponse:
    plugin = get_extensions_manager().get_plugin(plugin_name)
    if plugin is None:
        msg = pgettext_lazy("Dashboard message", "Selected plugin does not exist.")
        messages.error(request, msg)
        raise Http404()

    form = GatewayConfigurationForm(plugin, request.POST or None)
    if form.is_valid():
        form.save()
        msg = pgettext_lazy("Dashboard message", "Payment config succesfully updated")
        messages.success(request, msg)
        return redirect("dashboard:payments-index")

    ctx = {"plugin_name": plugin_name, "config_form": form}
    return TemplateResponse(request, "dashboard/payments/configuration_form.html", ctx)
