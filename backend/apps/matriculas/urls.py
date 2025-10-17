from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HealthCheckView,
    PlanoMensalidadeViewSet,
    PropostaMatriculaViewSet,
    MatriculaViewSet,
)

router = DefaultRouter()
router.register(r"planos", PlanoMensalidadeViewSet, basename="planos")
router.register(r"propostas", PropostaMatriculaViewSet, basename="propostas")
router.register(r"matriculas", MatriculaViewSet, basename="matriculas")

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="matriculas-health"),
    path("", include(router.urls)),
]
