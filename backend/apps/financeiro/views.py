from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from datetime import date

from .models import Fatura, Baixa
from .serializers import FaturaSerializer, BaixaSerializer
from apps.matriculas.models import Matricula


class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok", "service": "financeiro"})


class BaseProtectedViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]


def _last_day_of_month(year: int, month: int) -> int:
    if month == 12:
        return 31
    from datetime import date as _d

    first_next = _d(year + (month // 12), (month % 12) + 1, 1)
    last = first_next - _d.resolution
    return last.day


def _add_months(d: date, months: int) -> date:
    year = d.year + (d.month - 1 + months) // 12
    month = (d.month - 1 + months) % 12 + 1
    day = min(d.day, _last_day_of_month(year, month))
    return date(year, month, day)


class FaturaViewSet(BaseProtectedViewSet):
    queryset = Fatura.objects.select_related("matricula", "matricula__plano").all().order_by("-competencia", "-id")
    serializer_class = FaturaSerializer
    filterset_fields = ["matricula", "status", "competencia", "vencimento"]
    search_fields = ["matricula__aluno__nome", "matricula__turma__nome"]

    @action(detail=False, methods=["post"], url_path=r"gerar_para_matricula/(?P<matricula_id>[^/.]+)")
    @transaction.atomic
    def gerar_para_matricula(self, request, matricula_id=None):
        try:
            matricula = Matricula.objects.select_related("plano").get(pk=matricula_id)
        except Matricula.DoesNotExist:
            return Response({"detail": "Matrícula não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        try:
            parcelas = int(request.query_params.get("parcelas", "12"))
            if parcelas <= 0:
                raise ValueError
        except ValueError:
            return Response({"detail": "Parâmetro 'parcelas' inválido."}, status=status.HTTP_400_BAD_REQUEST)

        mes_base_str = request.query_params.get("mes_base")
        if not mes_base_str:
            return Response({"detail": "Parâmetro 'mes_base' é obrigatório (YYYY-MM-01)."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            base_year, base_month, base_day = [int(p) for p in mes_base_str.split("-")]
            base_date = date(base_year, base_month, base_day)
        except Exception:
            return Response({"detail": "Formato inválido para 'mes_base' (use YYYY-MM-01)."}, status=status.HTTP_400_BAD_REQUEST)

        created = []
        for i in range(parcelas):
            competencia = _add_months(base_date.replace(day=1), i)
            # Mantém o dia de vencimento igual ao dia do 'mes_base', ajustando ao último dia do mês se necessário
            vencimento_dia = min(base_day, _last_day_of_month(competencia.year, competencia.month))
            vencimento = competencia.replace(day=vencimento_dia)

            fatura, _ = Fatura.objects.get_or_create(
                matricula=matricula,
                competencia=competencia,
                defaults={
                    "vencimento": vencimento,
                    "valor": matricula.plano.valor,
                    "desconto": 0,
                    "acrescimo": 0,
                    "status": Fatura.Status.ABERTA,
                },
            )
            created.append(fatura)

        return Response(FaturaSerializer(created, many=True).data, status=status.HTTP_201_CREATED)


class BaixaViewSet(BaseProtectedViewSet):
    queryset = Baixa.objects.select_related("fatura", "fatura__matricula").all().order_by("-id")
    serializer_class = BaixaSerializer
    filterset_fields = ["fatura", "data_pagamento"]
    search_fields = ["fatura__matricula__aluno__nome"]

    @action(detail=True, methods=["post"], url_path="baixar")
    @transaction.atomic
    def baixar(self, request, pk=None):
        fatura = Fatura.objects.filter(pk=pk).first()
        if not fatura:
            return Response({"detail": "Fatura não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        data_pagamento = request.data.get("data_pagamento")
        valor_pago = request.data.get("valor_pago")
        observacao = request.data.get("observacao")
        if not data_pagamento or not valor_pago:
            return Response({"detail": "Campos obrigatórios: data_pagamento, valor_pago."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from datetime import datetime
            from decimal import Decimal

            data_pag_dt = datetime.strptime(data_pagamento, "%Y-%m-%d").date()
            valor_pago_dec = Decimal(str(valor_pago))
        except Exception:
            return Response({"detail": "Formato inválido de data/valor."}, status=status.HTTP_400_BAD_REQUEST)

        baixa = Baixa.objects.create(
            fatura=fatura,
            data_pagamento=data_pag_dt,
            valor_pago=valor_pago_dec,
            observacao=observacao,
        )
        fatura.status = Fatura.Status.PAGA
        fatura.save(update_fields=["status"])

        return Response(BaixaSerializer(baixa).data, status=status.HTTP_201_CREATED)
