import csv
import io
from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.utils import timezone

from .models import PurchaseOrder

REQUIRED_COLUMNS = {"PO Code", "Date", "Vendor"}
DATE_FORMATS = ("%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d")


def _parse_date_value(raw):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"invalid date {raw!r}")


def _parse_optional_date(raw):
    raw = (raw or "").strip()
    return _parse_date_value(raw) if raw else None


def _parse_required_date(raw, field_name):
    raw = (raw or "").strip()
    if not raw:
        raise ValueError(f"missing {field_name}")
    return _parse_date_value(raw)


def _parse_decimal(raw):
    raw = (raw or "").replace(",", "").strip()
    if not raw:
        return Decimal("0")
    try:
        return Decimal(raw)
    except InvalidOperation:
        raise ValueError(f"invalid number {raw!r}")


class ImportResult:
    def __init__(self):
        self.created = 0
        self.updated = 0
        self.errors = []  # list of (row_number, message); row 0 = file-level error

    @property
    def ok(self):
        return self.created or self.updated


def import_purchase_orders(uploaded_file):
    raw = uploaded_file.read()
    content = raw.decode("utf-8-sig") if isinstance(raw, bytes) else raw
    reader = csv.DictReader(io.StringIO(content))

    result = ImportResult()

    if not reader.fieldnames:
        result.errors.append((0, "The file appears to be empty."))
        return result

    missing = REQUIRED_COLUMNS - set(reader.fieldnames)
    if missing:
        result.errors.append((0, f"Missing required column(s): {', '.join(sorted(missing))}"))
        return result

    for row_number, row in enumerate(reader, start=2):  # header is row 1
        po_code = (row.get("PO Code") or "").strip()
        if not po_code:
            continue  # blank trailing row

        try:
            vendor = (row.get("Vendor") or "").strip()
            if not vendor:
                raise ValueError("missing Vendor")

            defaults = {
                "order_date": _parse_required_date(row.get("Date"), "Date"),
                "delivery_date": _parse_optional_date(row.get("DLV Date")),
                "vendor": vendor,
                "project_code": (row.get("Project Code") or "").strip(),
                "payment_term": (row.get("Payment Term") or "").strip(),
                "currency": (row.get("Curr.") or "").strip(),
                "net_value": _parse_decimal(row.get("Net Value")),
                "total_qty": _parse_decimal(row.get("Total QTY")),
                "received_qty": _parse_decimal(row.get("RCV QTY")),
                "invoiced_value": _parse_decimal(row.get("Invoiced Value")),
                "paid_value": _parse_decimal(row.get("Paid Value")),
                "source_state": (row.get("State") or "").strip(),
                "dlv_status": (row.get("DLV Status") or "").strip(),
                "last_imported_at": timezone.now(),
            }
        except ValueError as exc:
            result.errors.append((row_number, str(exc)))
            continue

        _, created = PurchaseOrder.objects.update_or_create(po_code=po_code, defaults=defaults)
        if created:
            result.created += 1
        else:
            result.updated += 1

    return result
