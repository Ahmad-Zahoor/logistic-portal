from django.urls import path

from . import views

urlpatterns = [
    path("purchase-orders/", views.POListView.as_view(), name="po-list"),
    path("purchase-orders/upload/", views.POUploadView.as_view(), name="po-upload"),
    path("purchase-orders/<int:pk>/", views.PODetailView.as_view(), name="po-detail"),
    path("purchase-orders/<int:pk>/status/", views.POStatusUpdateView.as_view(), name="po-status-update"),
    path(
        "purchase-orders/<int:pk>/eta-status/",
        views.POETAStatusUpdateView.as_view(),
        name="po-eta-status-update",
    ),
]
