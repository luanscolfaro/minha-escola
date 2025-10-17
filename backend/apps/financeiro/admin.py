from django.contrib import admin
from .models import Fatura, Baixa


@admin.register(Fatura)
class FaturaAdmin(admin.ModelAdmin):
    list_display = ("id", "matricula", "competencia", "vencimento", "valor", "status")
    list_filter = ("status", "competencia", "vencimento")
    search_fields = ("matricula__aluno__nome", "matricula__turma__nome")
    ordering = ("-competencia", "-id")


@admin.register(Baixa)
class BaixaAdmin(admin.ModelAdmin):
    list_display = ("id", "fatura", "data_pagamento", "valor_pago")
    list_filter = ("data_pagamento",)
    search_fields = ("fatura__matricula__aluno__nome",)
    ordering = ("-id",)
