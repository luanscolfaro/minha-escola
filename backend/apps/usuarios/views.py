from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Usuario, Tipo
from .serializers import UsuarioSerializer


class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok", "service": "usuarios"})


class IsDiretoriaOuCoordenacao(permissions.BasePermission):
    message = "Apenas usuários da Diretoria ou Coordenação podem gerenciar usuários."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # Permite apenas Diretoria/Coordenação
        try:
            return user.tipo in {Tipo.DIRETORIA, Tipo.COORDENACAO}
        except AttributeError:
            return False


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.filter(ativo=True).order_by("id")
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated, IsDiretoriaOuCoordenacao]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["tipo", "is_active"]
    search_fields = ["username", "first_name", "last_name", "email", "cpf"]
