from django.contrib import admin

from .models import Customer, Driver, Shipment, Task, Vehicle


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "email", "phone")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("registration_number", "vehicle_type", "capacity_kg", "status")
    list_filter = ("status", "vehicle_type")
    search_fields = ("registration_number",)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "license_number", "status")
    list_filter = ("status",)
    search_fields = ("name", "license_number")


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "reference_number",
        "customer",
        "origin",
        "destination",
        "vehicle",
        "driver",
        "status",
        "scheduled_date",
    )
    list_filter = ("status", "scheduled_date")
    search_fields = ("reference_number", "origin", "destination", "customer__name")
    date_hierarchy = "scheduled_date"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task_type", "assigned_to", "shipment", "due_date", "priority", "status")
    list_filter = ("status", "priority", "task_type", "due_date")
    search_fields = ("title", "description")
    date_hierarchy = "due_date"
