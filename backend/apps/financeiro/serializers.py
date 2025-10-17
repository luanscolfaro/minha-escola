from rest_framework import serializers
from .models import Fatura, Baixa


class FaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fatura
        fields = [
            "id",
            "matricula",
            "competencia",
            "vencimento",
            "valor",
            "desconto",
            "acrescimo",
            "status",
            "criado_em",
        ]
        read_only_fields = ["id", "criado_em"]


class BaixaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baixa
        fields = [
            "id",
            "fatura",
            "data_pagamento",
            "valor_pago",
            "observacao",
            "criado_em",
        ]
        read_only_fields = ["id", "criado_em"]

