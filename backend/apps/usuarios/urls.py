from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthCheckView, UsuarioViewSet


router = DefaultRouter()
router.register(r"usuarios", UsuarioViewSet, basename="usuarios")

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="usuarios-health"),
    path("", include(router.urls)),
]
