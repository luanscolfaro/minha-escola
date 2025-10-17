from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Endereco, Responsavel, Aluno
from .serializers import EnderecoSerializer, ResponsavelSerializer, AlunoSerializer


class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok", "service": "core"})


class BaseProtectedViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]


class EnderecoViewSet(BaseProtectedViewSet):
    queryset = Endereco.objects.filter(ativo=True).order_by("-criado_em")
    serializer_class = EnderecoSerializer
    filterset_fields = ["cidade", "estado", "ativo"]
    search_fields = ["logradouro", "bairro", "cidade", "cep"]


class ResponsavelViewSet(BaseProtectedViewSet):
    queryset = Responsavel.objects.filter(ativo=True).order_by("-criado_em")
    serializer_class = ResponsavelSerializer
    filterset_fields = ["cpf", "ativo"]
    search_fields = ["nome", "cpf", "email", "telefone"]


class AlunoViewSet(BaseProtectedViewSet):
    queryset = Aluno.objects.filter(ativo=True).order_by("-criado_em")
    serializer_class = AlunoSerializer
    filterset_fields = ["matricula", "cpf", "ativo"]
    search_fields = ["nome", "matricula", "cpf"]
