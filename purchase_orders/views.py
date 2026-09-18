from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView

from .forms import POUploadForm
from .imports import import_purchase_orders
from .models import PurchaseOrder

ETA_STATUS_MAX_LENGTH = PurchaseOrder._meta.get_field("eta_status").max_length


def _redirect_next(request, fallback_url_name="po-list"):
    next_url = request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(next_url)
    return redirect(reverse(fallback_url_name))


class POListView(LoginRequiredMixin, ListView):
    model = PurchaseOrder
    template_name = "purchase_orders/po_list.html"
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get("status")
        vendor = self.request.GET.get("vendor")
        query = self.request.GET.get("q")
        if status:
            qs = qs.filter(status=status)
        if vendor:
            qs = qs.filter(vendor__icontains=vendor)
        if query:
            qs = qs.filter(
                Q(po_code__icontains=query)
                | Q(vendor__icontains=query)
                | Q(project_code__icontains=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = PurchaseOrder.Status.choices
        context["selected_status"] = self.request.GET.get("status", "")
        context["vendor_query"] = self.request.GET.get("vendor", "")
        context["query"] = self.request.GET.get("q", "")
        context["querystring"] = self.request.GET.urlencode()
        return context


class PODetailView(LoginRequiredMixin, DetailView):
    model = PurchaseOrder
    template_name = "purchase_orders/po_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = PurchaseOrder.Status.choices
        return context


class POUploadView(LoginRequiredMixin, FormView):
    template_name = "purchase_orders/po_upload.html"
    form_class = POUploadForm
    success_url = reverse_lazy("po-upload")

    def form_valid(self, form):
        result = import_purchase_orders(form.cleaned_data["file"])

        if result.ok:
            messages.success(
                self.request,
                f"Import complete: {result.created} PO(s) created, {result.updated} updated.",
            )
        for row_number, error in result.errors[:20]:
            label = "File" if row_number == 0 else f"Row {row_number}"
            messages.error(self.request, f"{label}: {error}")
        if len(result.errors) > 20:
            messages.warning(self.request, f"…and {len(result.errors) - 20} more row error(s).")
        if not result.ok and not result.errors:
            messages.warning(self.request, "No rows were found in that file.")

        return super().form_valid(form)


class POStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        po = get_object_or_404(PurchaseOrder, pk=pk)
        status = request.POST.get("status")
        valid_statuses = dict(PurchaseOrder.Status.choices)
        if status in valid_statuses:
            po.status = status
            po.save(update_fields=["status", "updated_at"])
            messages.success(request, f"{po.po_code} marked as {valid_statuses[status]}.")
        else:
            messages.error(request, "Invalid status.")

        return _redirect_next(request)


class POETAStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        po = get_object_or_404(PurchaseOrder, pk=pk)
        eta_status = request.POST.get("eta_status", "").strip()
        if len(eta_status) > ETA_STATUS_MAX_LENGTH:
            messages.error(request, f"ETA status is too long (max {ETA_STATUS_MAX_LENGTH} characters).")
        else:
            po.eta_status = eta_status
            po.save(update_fields=["eta_status", "updated_at"])
            messages.success(request, f"{po.po_code} ETA status updated.")

        return _redirect_next(request)
