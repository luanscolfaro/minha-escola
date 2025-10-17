from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "tipo",
            "cpf",
            "telefone",
            "is_active",
            "ativo",
            "last_login",
            "date_joined",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "last_login", "date_joined", "created_at", "updated_at"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = Usuario(**validated_data)
        if password:
            user.set_password(password)
        else:
            # Garante que a senha não fique em texto puro
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            if password:
                instance.set_password(password)
            else:
                instance.set_unusable_password()
        instance.save()
        return instance

