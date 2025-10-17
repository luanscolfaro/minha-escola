from rest_framework import serializers
from .models import PlanoMensalidade, PropostaMatricula, Matricula


class PlanoMensalidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoMensalidade
        fields = ["id", "nome", "descricao", "valor", "ativo", "criado_em"]
        read_only_fields = ["id", "criado_em"]


class PropostaMatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropostaMatricula
        fields = ["id", "aluno", "observacao", "status", "criado_em"]
        read_only_fields = ["id", "criado_em"]


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = ["id", "aluno", "turma", "plano", "ano_letivo", "ativa", "criado_em"]
        read_only_fields = ["id", "criado_em"]

