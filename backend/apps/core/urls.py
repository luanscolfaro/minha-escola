from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthCheckView, EnderecoViewSet, ResponsavelViewSet, AlunoViewSet

router = DefaultRouter()
router.register(r"enderecos", EnderecoViewSet, basename="enderecos")
router.register(r"responsaveis", ResponsavelViewSet, basename="responsaveis")
router.register(r"alunos", AlunoViewSet, basename="alunos")

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="core-health"),
    path("", include(router.urls)),
]
