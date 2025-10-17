from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HealthCheckView,
    SerieViewSet,
    DisciplinaViewSet,
    TurmaViewSet,
    AlocacaoViewSet,
    AulaViewSet,
    PresencaViewSet,
    AvaliacaoViewSet,
    NotaViewSet,
)

router = DefaultRouter()
router.register(r"series", SerieViewSet, basename="series")
router.register(r"disciplinas", DisciplinaViewSet, basename="disciplinas")
router.register(r"turmas", TurmaViewSet, basename="turmas")
router.register(r"alocacoes", AlocacaoViewSet, basename="alocacoes")
router.register(r"aulas", AulaViewSet, basename="aulas")
router.register(r"presencas", PresencaViewSet, basename="presencas")
router.register(r"avaliacoes", AvaliacaoViewSet, basename="avaliacoes")
router.register(r"notas", NotaViewSet, basename="notas")

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="academico-health"),
    path("", include(router.urls)),
]
