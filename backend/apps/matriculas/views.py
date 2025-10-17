from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from .models import PlanoMensalidade, PropostaMatricula, Matricula
from .serializers import (
    PlanoMensalidadeSerializer,
    PropostaMatriculaSerializer,
    MatriculaSerializer,
)


class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok", "service": "matriculas"})


class BaseProtectedViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]


class PlanoMensalidadeViewSet(BaseProtectedViewSet):
    queryset = PlanoMensalidade.objects.filter(ativo=True).order_by("nome")
    serializer_class = PlanoMensalidadeSerializer
    filterset_fields = ["ativo"]
    search_fields = ["nome", "descricao"]


class PropostaMatriculaViewSet(BaseProtectedViewSet):
    queryset = PropostaMatricula.objects.select_related("aluno").all().order_by("-id")
    serializer_class = PropostaMatriculaSerializer
    filterset_fields = ["status", "aluno"]
    search_fields = ["aluno__nome"]

    @action(detail=True, methods=["post"], url_path="aprovar_proposta")
    @transaction.atomic
    def aprovar_proposta(self, request, pk=None):
        proposta = self.get_object()
        if proposta.status != PropostaMatricula.Status.ABERTA:
            return Response({"detail": "A proposta não está em status ABERTA."}, status=status.HTTP_400_BAD_REQUEST)

        turma_id = request.data.get("turma")
        plano_id = request.data.get("plano")
        ano_letivo = request.data.get("ano_letivo")

        if not turma_id or not plano_id or not ano_letivo:
            return Response({"detail": "Campos obrigatórios: turma, plano, ano_letivo."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from apps.academico.models import Turma

            turma = Turma.objects.get(pk=turma_id)
        except Exception:
            return Response({"detail": "Turma não encontrada."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            plano = PlanoMensalidade.objects.get(pk=plano_id)
        except PlanoMensalidade.DoesNotExist:
            return Response({"detail": "Plano não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        matricula, created = Matricula.objects.get_or_create(
            aluno=proposta.aluno,
            turma=turma,
            ano_letivo=ano_letivo,
            defaults={"plano": plano, "ativa": True},
        )
        if not created:
            # Garante que o plano esteja atualizado e ativa a matrícula
            matricula.plano = plano
            matricula.ativa = True
            matricula.save()

        proposta.status = PropostaMatricula.Status.APROVADA
        proposta.save(update_fields=["status"])

        return Response(MatriculaSerializer(matricula).data, status=status.HTTP_201_CREATED)


class MatriculaViewSet(BaseProtectedViewSet):
    queryset = (
        Matricula.objects.select_related("aluno", "turma", "plano").filter(ativa=True).order_by("-id")
    )
    serializer_class = MatriculaSerializer
    filterset_fields = ["aluno", "turma", "plano", "ano_letivo", "ativa"]
    search_fields = ["aluno__nome", "turma__nome"]
