from django.db import models
from django.conf import settings

from apps.usuarios.models import Usuario, Tipo
from apps.core.models import Aluno


class Serie(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.nome


class Disciplina(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.nome


class Turma(models.Model):
    nome = models.CharField(max_length=120)
    serie = models.ForeignKey(Serie, on_delete=models.PROTECT, related_name="turmas")
    ano_letivo = models.IntegerField()
    turno = models.CharField(max_length=20, blank=True, null=True)
    professores = models.ManyToManyField(
        Usuario,
        blank=True,
        related_name="turmas",
        limit_choices_to={"tipo": Tipo.PROFESSOR},
    )
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("nome", "serie", "ano_letivo")

    def __str__(self) -> str:
        return f"{self.nome} - {self.serie.nome}/{self.ano_letivo}"


class Alocacao(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="alocacoes")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT, related_name="alocacoes")
    professor = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name="alocacoes",
        limit_choices_to={"tipo": Tipo.PROFESSOR},
    )
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("turma", "disciplina", "professor")

    def __str__(self) -> str:
        return f"{self.turma} - {self.disciplina} ({self.professor})"


class Aula(models.Model):
    alocacao = models.ForeignKey(Alocacao, on_delete=models.CASCADE, related_name="aulas")
    data = models.DateField()
    conteudo = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data", "-id"]
        unique_together = ("alocacao", "data")

    def __str__(self) -> str:
        return f"Aula {self.data} - {self.alocacao}"


class Presenca(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name="presencas")
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="presencas")
    presente = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("aula", "aluno")

    def __str__(self) -> str:
        status = "Presente" if self.presente else "Ausente"
        return f"{self.aluno} - {self.aula} - {status}"


class Avaliacao(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="avaliacoes")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT, related_name="avaliacoes")
    titulo = models.CharField(max_length=120)
    data = models.DateField()
    peso = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("turma", "disciplina", "titulo", "data")

    def __str__(self) -> str:
        return f"{self.titulo} - {self.turma}/{self.disciplina}"


class Nota(models.Model):
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name="notas")
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="notas")
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    observacao = models.CharField(max_length=255, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("avaliacao", "aluno")

    def __str__(self) -> str:
        return f"{self.aluno} - {self.avaliacao}: {self.valor}"

