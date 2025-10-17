from django.db import models
from django.contrib.auth.models import AbstractUser


class Tipo(models.TextChoices):
    DIRETORIA = "DIRETORIA", "Diretoria"
    COORDENACAO = "COORDENACAO", "Coordenação"
    SECRETARIA = "SECRETARIA", "Secretaria"
    PROFESSOR = "PROFESSOR", "Professor"
    RESPONSAVEL = "RESPONSAVEL", "Responsável"
    ALUNO = "ALUNO", "Aluno"


class Usuario(AbstractUser):
    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
        default=Tipo.ALUNO,
        db_index=True,
    )
    cpf = models.CharField(max_length=14, unique=True, db_index=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Mantém is_active em sincronia com 'ativo'
        self.is_active = self.ativo
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.username} ({self.get_tipo_display()})"

