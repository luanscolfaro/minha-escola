from django.contrib import admin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "tipo",
        "cpf",
        "is_active",
        "ativo",
    )
    list_filter = ("tipo", "is_active", "ativo")
    search_fields = ("username", "first_name", "last_name", "email", "cpf")
    ordering = ("id",)
