from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Serie, Disciplina, Turma, Alocacao, Aula, Presenca, Avaliacao, Nota
from .serializers import (
    SerieSerializer,
    DisciplinaSerializer,
    TurmaSerializer,
    AlocacaoSerializer,
    AulaSerializer,
    PresencaSerializer,
    AvaliacaoSerializer,
    NotaSerializer,
)


class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok", "service": "academico"})


class BaseProtectedViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]


class SerieViewSet(BaseProtectedViewSet):
    queryset = Serie.objects.filter(ativo=True).order_by("nome")
    serializer_class = SerieSerializer
    filterset_fields = ["ativo"]
    search_fields = ["nome", "descricao"]


class DisciplinaViewSet(BaseProtectedViewSet):
    queryset = Disciplina.objects.filter(ativo=True).order_by("nome")
    serializer_class = DisciplinaSerializer
    filterset_fields = ["ativo"]
    search_fields = ["nome", "descricao"]


class TurmaViewSet(BaseProtectedViewSet):
    queryset = (
        Turma.objects.select_related("serie").prefetch_related("professores").filter(ativo=True).order_by("-ano_letivo", "nome")
    )
    serializer_class = TurmaSerializer
    filterset_fields = ["serie", "ano_letivo", "turno", "ativo"]
    search_fields = ["nome"]


class AlocacaoViewSet(BaseProtectedViewSet):
    queryset = (
        Alocacao.objects.select_related("turma", "disciplina", "professor").filter(ativo=True).order_by("-id")
    )
    serializer_class = AlocacaoSerializer
    filterset_fields = ["turma", "disciplina", "professor", "ativo"]
    search_fields = ["turma__nome", "disciplina__nome", "professor__username", "professor__first_name", "professor__last_name"]


class AulaViewSet(BaseProtectedViewSet):
    queryset = Aula.objects.select_related("alocacao", "alocacao__turma", "alocacao__disciplina").all().order_by("-data", "-id")
    serializer_class = AulaSerializer
    filterset_fields = ["alocacao", "data"]
    search_fields = ["conteudo"]


class PresencaViewSet(BaseProtectedViewSet):
    queryset = Presenca.objects.select_related("aula", "aluno").all().order_by("-id")
    serializer_class = PresencaSerializer
    filterset_fields = ["aula", "aluno", "presente"]
    search_fields = ["aluno__nome"]


class AvaliacaoViewSet(BaseProtectedViewSet):
    queryset = Avaliacao.objects.select_related("turma", "disciplina").all().order_by("-data", "-id")
    serializer_class = AvaliacaoSerializer
    filterset_fields = ["turma", "disciplina", "data"]
    search_fields = ["titulo", "disciplina__nome", "turma__nome"]


class NotaViewSet(BaseProtectedViewSet):
    queryset = Nota.objects.select_related("avaliacao", "aluno", "avaliacao__turma", "avaliacao__disciplina").all().order_by("-id")
    serializer_class = NotaSerializer
    filterset_fields = ["avaliacao", "aluno"]
    search_fields = ["aluno__nome"]
