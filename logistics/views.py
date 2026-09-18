from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import CustomerForm, DriverForm, ShipmentForm, TaskForm, VehicleForm
from .models import Customer, Driver, Shipment, Task, Vehicle


class GenericFormTemplateMixin:
    template_name = "logistics/object_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model._meta.verbose_name
        return context


class GenericDeleteTemplateMixin:
    template_name = "logistics/object_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model._meta.verbose_name
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "logistics/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        context["today"] = today
        context["todays_tasks"] = (
            Task.objects.filter(due_date=today).exclude(status=Task.Status.COMPLETED)
        )
        context["overdue_tasks"] = (
            Task.objects.filter(due_date__lt=today).exclude(
                status__in=[Task.Status.COMPLETED, Task.Status.CANCELLED]
            )
        )
        context["active_shipments"] = Shipment.objects.filter(
            status__in=[Shipment.Status.PENDING, Shipment.Status.PICKED_UP, Shipment.Status.IN_TRANSIT]
        )
        context["task_count"] = Task.objects.exclude(
            status__in=[Task.Status.COMPLETED, Task.Status.CANCELLED]
        ).count()
        context["shipment_count"] = context["active_shipments"].count()
        context["available_vehicles"] = Vehicle.objects.filter(status=Vehicle.Status.AVAILABLE).count()
        context["available_drivers"] = Driver.objects.filter(status=Driver.Status.AVAILABLE).count()
        return context


# ---- Task ----

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().select_related("shipment", "assigned_to")
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Task.Status.choices
        context["selected_status"] = self.request.GET.get("status", "")
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, GenericFormTemplateMixin, CreateView):
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, GenericFormTemplateMixin, UpdateView):
    model = Task
    form_class = TaskForm


class TaskDeleteView(LoginRequiredMixin, GenericDeleteTemplateMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task-list")


# ---- Shipment ----

class ShipmentListView(LoginRequiredMixin, ListView):
    model = Shipment
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().select_related("customer", "vehicle", "driver")
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Shipment.Status.choices
        context["selected_status"] = self.request.GET.get("status", "")
        return context


class ShipmentDetailView(LoginRequiredMixin, DetailView):
    model = Shipment


class ShipmentCreateView(LoginRequiredMixin, GenericFormTemplateMixin, CreateView):
    model = Shipment
    form_class = ShipmentForm


class ShipmentUpdateView(LoginRequiredMixin, GenericFormTemplateMixin, UpdateView):
    model = Shipment
    form_class = ShipmentForm


class ShipmentDeleteView(LoginRequiredMixin, GenericDeleteTemplateMixin, DeleteView):
    model = Shipment
    success_url = reverse_lazy("shipment-list")


# ---- Vehicle ----

class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    paginate_by = 25


class VehicleDetailView(LoginRequiredMixin, DetailView):
    model = Vehicle


class VehicleCreateView(LoginRequiredMixin, GenericFormTemplateMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm


class VehicleUpdateView(LoginRequiredMixin, GenericFormTemplateMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm


class VehicleDeleteView(LoginRequiredMixin, GenericDeleteTemplateMixin, DeleteView):
    model = Vehicle
    success_url = reverse_lazy("vehicle-list")


# ---- Driver ----

class DriverListView(LoginRequiredMixin, ListView):
    model = Driver
    paginate_by = 25


class DriverDetailView(LoginRequiredMixin, DetailView):
    model = Driver


class DriverCreateView(LoginRequiredMixin, GenericFormTemplateMixin, CreateView):
    model = Driver
    form_class = DriverForm


class DriverUpdateView(LoginRequiredMixin, GenericFormTemplateMixin, UpdateView):
    model = Driver
    form_class = DriverForm


class DriverDeleteView(LoginRequiredMixin, GenericDeleteTemplateMixin, DeleteView):
    model = Driver
    success_url = reverse_lazy("driver-list")


# ---- Customer ----

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    paginate_by = 25


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer


class CustomerCreateView(LoginRequiredMixin, GenericFormTemplateMixin, CreateView):
    model = Customer
    form_class = CustomerForm


class CustomerUpdateView(LoginRequiredMixin, GenericFormTemplateMixin, UpdateView):
    model = Customer
    form_class = CustomerForm


class CustomerDeleteView(LoginRequiredMixin, GenericDeleteTemplateMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy("customer-list")
