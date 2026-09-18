from django.conf import settings
from django.db import models
from django.urls import reverse


class Customer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("customer-detail", args=[self.pk])


class Vehicle(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        IN_USE = "in_use", "In use"
        MAINTENANCE = "maintenance", "In maintenance"

    registration_number = models.CharField(max_length=30, unique=True)
    vehicle_type = models.CharField(max_length=50, blank=True)
    capacity_kg = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

    class Meta:
        ordering = ["registration_number"]

    def __str__(self):
        return self.registration_number

    def get_absolute_url(self):
        return reverse("vehicle-detail", args=[self.pk])


class Driver(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        ON_DUTY = "on_duty", "On duty"
        OFF_DUTY = "off_duty", "Off duty"

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("driver-detail", args=[self.pk])


class Shipment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PICKED_UP = "picked_up", "Picked up"
        IN_TRANSIT = "in_transit", "In transit"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    reference_number = models.CharField(max_length=30, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="shipments")
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name="shipments"
    )
    driver = models.ForeignKey(
        Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name="shipments"
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    scheduled_date = models.DateField()
    delivered_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-scheduled_date"]

    def __str__(self):
        return self.reference_number

    def get_absolute_url(self):
        return reverse("shipment-detail", args=[self.pk])


class Task(models.Model):
    class TaskType(models.TextChoices):
        PICKUP = "pickup", "Pickup"
        DELIVERY = "delivery", "Delivery"
        MAINTENANCE = "maintenance", "Maintenance"
        OTHER = "other", "Other"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=20, choices=TaskType.choices, default=TaskType.OTHER)
    shipment = models.ForeignKey(
        Shipment, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    assigned_to = models.ForeignKey(
        Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["due_date", "-priority"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("task-detail", args=[self.pk])
