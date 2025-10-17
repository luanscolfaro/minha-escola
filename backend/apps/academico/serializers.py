from rest_framework import serializers
from .models import Serie, Disciplina, Turma, Alocacao, Aula, Presenca, Avaliacao, Nota


class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serie
        fields = ["id", "nome", "descricao", "ativo", "criado_em"]
        read_only_fields = ["id", "criado_em"]


class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = ["id", "nome", "descricao", "ativo", "criado_em"]
        read_only_fields = ["id", "criado_em"]


class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = [
            "id",
            "nome",
            "serie",
            "ano_letivo",
            "turno",
            "professores",
            "ativo",
            "criado_em",
        ]
        read_only_fields = ["id", "criado_em"]


class AlocacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alocacao
        fields = ["id", "turma", "disciplina", "professor", "ativo", "criado_em"]
        read_only_fields = ["id", "criado_em"]


class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = ["id", "alocacao", "data", "conteudo", "criado_em"]
        read_only_fields = ["id", "criado_em"]


class PresencaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presenca
        fields = ["id", "aula", "aluno", "presente", "criado_em"]
        read_only_fields = ["id", "criado_em"]


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ["id", "turma", "disciplina", "titulo", "data", "peso", "criado_em"]
        read_only_fields = ["id", "criado_em"]


class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = ["id", "avaliacao", "aluno", "valor", "observacao", "criado_em"]
        read_only_fields = ["id", "criado_em"]

