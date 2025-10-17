from django.db import models
from decimal import Decimal

from apps.matriculas.models import Matricula


class Fatura(models.Model):
    class Status(models.TextChoices):
        ABERTA = "ABERTA", "Aberta"
        PAGA = "PAGA", "Paga"
        ATRASADA = "ATRASADA", "Atrasada"
        CANCELADA = "CANCELADA", "Cancelada"

    matricula = models.ForeignKey(Matricula, on_delete=models.PROTECT, related_name="faturas")
    competencia = models.DateField(help_text="Mês/competência da fatura (ex.: 2025-01-01)")
    vencimento = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    acrescimo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTA, db_index=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("matricula", "competencia")
        ordering = ["-competencia", "-id"]

    def __str__(self) -> str:
        return f"Fatura {self.matricula} - {self.competencia} ({self.status})"


class Baixa(models.Model):
    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE, related_name="baixas")
    data_pagamento = models.DateField()
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.CharField(max_length=255, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Baixa {self.fatura_id} - {self.data_pagamento} ({self.valor_pago})"

