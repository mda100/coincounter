from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddressViewSet, TransactionCreateView

router = DefaultRouter()
router.register("addresses", AddressViewSet, basename='address')

urlpatterns = [
    path("", include(router.urls)),
    path("transactions/", TransactionCreateView.as_view(), name="transaction-create"),
]
