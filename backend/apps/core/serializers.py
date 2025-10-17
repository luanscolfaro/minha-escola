from rest_framework import serializers
from .models import Endereco, Responsavel, Aluno


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = [
            "id",
            "logradouro",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "estado",
            "cep",
            "ativo",
            "criado_em",
        ]
        read_only_fields = ["id", "criado_em"]


class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = [
            "id",
            "nome",
            "cpf",
            "telefone",
            "email",
            "endereco",
            "ativo",
            "criado_em",
        ]
        read_only_fields = ["id", "criado_em"]


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = [
            "id",
            "nome",
            "matricula",
            "cpf",
            "data_nascimento",
            "responsavel",
            "endereco",
            "ativo",
            "criado_em",
        ]
        read_only_fields = ["id", "criado_em"]

