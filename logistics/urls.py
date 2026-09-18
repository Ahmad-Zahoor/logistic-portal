from django.urls import path

from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    # Tasks
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path("tasks/new/", views.TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task-delete"),
    # Shipments
    path("shipments/", views.ShipmentListView.as_view(), name="shipment-list"),
    path("shipments/new/", views.ShipmentCreateView.as_view(), name="shipment-create"),
    path("shipments/<int:pk>/", views.ShipmentDetailView.as_view(), name="shipment-detail"),
    path("shipments/<int:pk>/edit/", views.ShipmentUpdateView.as_view(), name="shipment-update"),
    path("shipments/<int:pk>/delete/", views.ShipmentDeleteView.as_view(), name="shipment-delete"),
    # Vehicles
    path("vehicles/", views.VehicleListView.as_view(), name="vehicle-list"),
    path("vehicles/new/", views.VehicleCreateView.as_view(), name="vehicle-create"),
    path("vehicles/<int:pk>/", views.VehicleDetailView.as_view(), name="vehicle-detail"),
    path("vehicles/<int:pk>/edit/", views.VehicleUpdateView.as_view(), name="vehicle-update"),
    path("vehicles/<int:pk>/delete/", views.VehicleDeleteView.as_view(), name="vehicle-delete"),
    # Drivers
    path("drivers/", views.DriverListView.as_view(), name="driver-list"),
    path("drivers/new/", views.DriverCreateView.as_view(), name="driver-create"),
    path("drivers/<int:pk>/", views.DriverDetailView.as_view(), name="driver-detail"),
    path("drivers/<int:pk>/edit/", views.DriverUpdateView.as_view(), name="driver-update"),
    path("drivers/<int:pk>/delete/", views.DriverDeleteView.as_view(), name="driver-delete"),
    # Customers
    path("customers/", views.CustomerListView.as_view(), name="customer-list"),
    path("customers/new/", views.CustomerCreateView.as_view(), name="customer-create"),
    path("customers/<int:pk>/", views.CustomerDetailView.as_view(), name="customer-detail"),
    path("customers/<int:pk>/edit/", views.CustomerUpdateView.as_view(), name="customer-update"),
    path("customers/<int:pk>/delete/", views.CustomerDeleteView.as_view(), name="customer-delete"),
]
