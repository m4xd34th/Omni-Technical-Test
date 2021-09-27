from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ClientViewset,
    Login,
    Logout,
    OrderViewset,
    PaymentViewset,
    ProductViewset,
    RefreshToken,
    ShipmentViewset,
)

router = DefaultRouter()
router.register(r"client", ClientViewset, basename="list")
router.register(r"order", OrderViewset)
router.register(r"payment", PaymentViewset)
router.register(r"product", ProductViewset)
router.register(r"shipment", ShipmentViewset)

urlpatterns = [
    path("store/", include(router.urls), name="rest-api"),
    path("login/", Login.as_view(), name="Rest-Login"),
    path("refresh-token/", RefreshToken.as_view(), name="Rest-Refresh"),
    path("logout/", Logout.as_view(), name="Rest-Logout"),
]
