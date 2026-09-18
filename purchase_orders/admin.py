from django.contrib import admin

from .models import PurchaseOrder


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = (
        "po_code",
        "vendor",
        "project_code",
        "order_date",
        "delivery_date",
        "net_value",
        "status",
        "source_state",
        "dlv_status",
    )
    list_filter = ("status", "source_state", "dlv_status", "currency")
    search_fields = ("po_code", "vendor", "project_code")
    date_hierarchy = "order_date"
