from django.db import models


class Endereco(models.Model):
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20, blank=True, null=True)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=120, blank=True, null=True)
    cidade = models.CharField(max_length=120)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        n = f", {self.numero}" if self.numero else ""
        c = f" - {self.complemento}" if self.complemento else ""
        return f"{self.logradouro}{n}{c}, {self.bairro or ''} - {self.cidade}/{self.estado}"


class Responsavel(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, blank=True, related_name="responsaveis")

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.nome} ({self.cpf})"


class Aluno(models.Model):
    nome = models.CharField(max_length=150)
    matricula = models.CharField(max_length=50, unique=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.SET_NULL, null=True, blank=True, related_name="alunos")
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, blank=True, related_name="alunos")

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.nome} ({self.matricula})"

