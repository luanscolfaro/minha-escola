from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthCheckView, FaturaViewSet, BaixaViewSet

router = DefaultRouter()
router.register(r"faturas", FaturaViewSet, basename="faturas")
router.register(r"baixas", BaixaViewSet, basename="baixas")

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="financeiro-health"),
    path("", include(router.urls)),
]
