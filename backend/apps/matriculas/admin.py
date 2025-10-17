from django.contrib import admin
from .models import PlanoMensalidade, PropostaMatricula, Matricula


@admin.register(PlanoMensalidade)
class PlanoMensalidadeAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "valor", "ativo")
    list_filter = ("ativo",)
    search_fields = ("nome",)
    ordering = ("nome",)


@admin.register(PropostaMatricula)
class PropostaMatriculaAdmin(admin.ModelAdmin):
    list_display = ("id", "aluno", "status", "criado_em")
    list_filter = ("status",)
    search_fields = ("aluno__nome",)
    ordering = ("-id",)


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ("id", "aluno", "turma", "plano", "ano_letivo", "ativa")
    list_filter = ("ano_letivo", "ativa")
    search_fields = ("aluno__nome", "turma__nome")
    ordering = ("-id",)
