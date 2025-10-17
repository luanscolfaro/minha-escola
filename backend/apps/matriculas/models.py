from django.db import models
from apps.core.models import Aluno
from apps.academico.models import Turma


class PlanoMensalidade(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    descricao = models.TextField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.nome} (R$ {self.valor})"


class PropostaMatricula(models.Model):
    class Status(models.TextChoices):
        ABERTA = "ABERTA", "Aberta"
        APROVADA = "APROVADA", "Aprovada"
        REPROVADA = "REPROVADA", "Reprovada"
        CANCELADA = "CANCELADA", "Cancelada"

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="propostas")
    observacao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTA, db_index=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Proposta {self.id} - {self.aluno} [{self.status}]"


class Matricula(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="matriculas")
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT, related_name="matriculas")
    plano = models.ForeignKey(PlanoMensalidade, on_delete=models.PROTECT, related_name="matriculas")
    ano_letivo = models.IntegerField()
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("aluno", "turma", "ano_letivo")

    def __str__(self) -> str:
        return f"{self.aluno} - {self.turma} ({self.ano_letivo})"

