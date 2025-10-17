from django.core.management.base import BaseCommand
from django.db import transaction

from apps.usuarios.models import Usuario, Tipo
from apps.core.models import Endereco, Responsavel, Aluno
from apps.academico.models import Serie, Disciplina


class Command(BaseCommand):
    help = "Cria dados iniciais: usuários base, séries/disciplinas padrão e alguns responsáveis/alunos."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("[Seeds] Criando usuários base..."))

        def ensure_user(username: str, email: str, tipo: str, cpf: str, is_staff=False, is_superuser=False, password: str = "senha123"):
            user, created = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "tipo": tipo,
                    "cpf": cpf,
                    "is_staff": is_staff,
                    "is_superuser": is_superuser,
                    "first_name": username.capitalize(),
                },
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f" - Usuário criado: {username} ({tipo})"))
            else:
                self.stdout.write(f" - Usuário já existe: {username}")
            return user

        ensure_user("admin", "admin@local", Tipo.DIRETORIA, "000.000.000-00", is_staff=True, is_superuser=True, password="admin123")
        ensure_user("diretoria", "diretoria@local", Tipo.DIRETORIA, "000.000.000-01", is_staff=True)
        ensure_user("coordenacao", "coordenacao@local", Tipo.COORDENACAO, "000.000.000-02", is_staff=True)
        ensure_user("secretaria", "secretaria@local", Tipo.SECRETARIA, "000.000.000-03", is_staff=True)
        ensure_user("professor", "professor@local", Tipo.PROFESSOR, "000.000.000-04", is_staff=True)

        self.stdout.write(self.style.MIGRATE_HEADING("[Seeds] Criando séries e disciplinas..."))

        series = [
            ("Educação Infantil (EI)", ""),
            ("Ensino Fundamental I (EF I)", ""),
            ("Ensino Fundamental II (EF II)", ""),
            ("Ensino Médio (EM)", ""),
        ]
        for nome, desc in series:
            Serie.objects.get_or_create(nome=nome, defaults={"descricao": desc})

        disciplinas = [
            ("Português", "Língua Portuguesa"),
            ("Matemática", "Matemática"),
            ("Ciências", "Ciências"),
            ("História", "História"),
            ("Geografia", "Geografia"),
            ("Inglês", "Língua Inglesa"),
        ]
        for nome, desc in disciplinas:
            Disciplina.objects.get_or_create(nome=nome, defaults={"descricao": desc})

        self.stdout.write(self.style.MIGRATE_HEADING("[Seeds] Criando responsáveis, endereços e alunos..."))

        end1, _ = Endereco.objects.get_or_create(
            logradouro="Rua das Flores",
            numero="123",
            cidade="Fortaleza",
            estado="CE",
            cep="60000-000",
            defaults={"bairro": "Centro"},
        )
        end2, _ = Endereco.objects.get_or_create(
            logradouro="Av. Atlântica",
            numero="500",
            cidade="Fortaleza",
            estado="CE",
            cep="60100-000",
            defaults={"bairro": "Praia"},
        )

        resp1, _ = Responsavel.objects.get_or_create(
            cpf="111.111.111-11",
            defaults={
                "nome": "Maria Silva",
                "telefone": "(85) 99999-1111",
                "email": "maria.silva@local",
                "endereco": end1,
            },
        )
        resp2, _ = Responsavel.objects.get_or_create(
            cpf="222.222.222-22",
            defaults={
                "nome": "João Souza",
                "telefone": "(85) 98888-2222",
                "email": "joao.souza@local",
                "endereco": end2,
            },
        )

        Aluno.objects.get_or_create(
            matricula="A0001",
            defaults={
                "nome": "Ana Silva",
                "cpf": "333.333.333-33",
                "responsavel": resp1,
                "endereco": end1,
            },
        )
        Aluno.objects.get_or_create(
            matricula="A0002",
            defaults={
                "nome": "Bruno Souza",
                "cpf": "444.444.444-44",
                "responsavel": resp2,
                "endereco": end2,
            },
        )
        Aluno.objects.get_or_create(
            matricula="A0003",
            defaults={
                "nome": "Carla Oliveira",
                "cpf": "555.555.555-55",
                "responsavel": resp1,
                "endereco": end1,
            },
        )

        self.stdout.write(self.style.SUCCESS("Seeds concluídos com sucesso."))

