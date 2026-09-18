from decimal import Decimal

from django.db import models
from django.urls import reverse


class PurchaseOrder(models.Model):
    class Status(models.TextChoices):
        PENDING_REVIEW = "pending_review", "Pending review"
        IN_PROGRESS = "in_progress", "In progress"
        ON_HOLD = "on_hold", "On hold"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    # Fields sourced from the daily uploaded sheet — overwritten on every import.
    po_code = models.CharField(max_length=50, unique=True)
    order_date = models.DateField()
    delivery_date = models.DateField(null=True, blank=True)
    vendor = models.CharField(max_length=255)
    project_code = models.CharField(max_length=50, blank=True)
    payment_term = models.CharField(max_length=255, blank=True)
    currency = models.CharField(max_length=10, blank=True)
    net_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_qty = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    received_qty = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    invoiced_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    paid_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    source_state = models.CharField(max_length=50, blank=True)
    dlv_status = models.CharField(max_length=50, blank=True)
    last_imported_at = models.DateTimeField(null=True, blank=True)

    # Managed by hand in the portal — re-importing the sheet never touches this.
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING_REVIEW)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-order_date", "po_code"]

    def __str__(self):
        return self.po_code

    def get_absolute_url(self):
        return reverse("po-detail", args=[self.pk])

    @property
    def received_pct(self):
        if not self.total_qty:
            return Decimal("0")
        return (self.received_qty / self.total_qty) * 100

    @property
    def invoiced_pct(self):
        if not self.net_value:
            return Decimal("0")
        return (self.invoiced_value / self.net_value) * 100

    @property
    def paid_pct(self):
        if not self.net_value:
            return Decimal("0")
        return (self.paid_value / self.net_value) * 100
