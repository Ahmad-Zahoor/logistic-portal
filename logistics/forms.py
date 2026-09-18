from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Customer, Driver, Shipment, Task, Vehicle

WIDGET_CLASS = "form-control"


def _styled_widgets(fields):
    widgets = {}
    for name, field in fields.items():
        css = "form-select" if isinstance(field.widget, (forms.Select, forms.SelectMultiple)) else WIDGET_CLASS
        field.widget.attrs.setdefault("class", css)
    return widgets


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styled_widgets(self.fields)


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styled_widgets(self.fields)


class CustomerForm(StyledModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email", "phone", "address"]


class VehicleForm(StyledModelForm):
    class Meta:
        model = Vehicle
        fields = ["registration_number", "vehicle_type", "capacity_kg", "status"]


class DriverForm(StyledModelForm):
    class Meta:
        model = Driver
        fields = ["name", "phone", "license_number", "status"]


class ShipmentForm(StyledModelForm):
    class Meta:
        model = Shipment
        fields = [
            "reference_number",
            "customer",
            "origin",
            "destination",
            "vehicle",
            "driver",
            "status",
            "scheduled_date",
            "notes",
        ]
        widgets = {
            "scheduled_date": forms.DateInput(attrs={"type": "date"}),
        }


class TaskForm(StyledModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "task_type",
            "shipment",
            "assigned_to",
            "due_date",
            "priority",
            "status",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
