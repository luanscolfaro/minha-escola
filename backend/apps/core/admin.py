from django.contrib import admin
from .models import Endereco, Responsavel, Aluno


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ("id", "logradouro", "numero", "cidade", "estado", "cep", "ativo")
    list_filter = ("estado", "cidade", "ativo")
    search_fields = ("logradouro", "bairro", "cidade", "cep")
    ordering = ("-id",)


@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "cpf", "telefone", "email", "ativo")
    list_filter = ("ativo",)
    search_fields = ("nome", "cpf", "email", "telefone")
    ordering = ("-id",)


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "matricula", "cpf", "responsavel", "ativo")
    list_filter = ("ativo",)
    search_fields = ("nome", "matricula", "cpf")
    ordering = ("-id",)
