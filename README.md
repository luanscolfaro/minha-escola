# Projeto Minha Escola

## Pré-requisitos
- Python 3.11 ou superior
- Pip atualizado (`pip install --upgrade pip`)
- (Opcional) Servidor MySQL para ambiente de produção

## Setup rápido
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
# source .venv/bin/activate

# Opção 1 (recomendada no Windows): usar SQLite e requirements-dev
pip install -r backend/requirements-dev.txt

# Opção 2 (MySQL): instalar dependências completas
# pip install -r backend/requirements.txt
```

## Estrutura
```
minha_escola/
  backend/
    manage.py
    escola/
      settings.py
      urls.py
      asgi.py
      wsgi.py
    apps/
      usuarios/
      core/
      academico/
      matriculas/
      financeiro/
      comunicacao/
      documentos/
    requirements.txt
  frontend/
    minha-escola-app/               # (criado via Angular CLI)
      src/app/
        core/interceptors/jwt.interceptor.ts
  README.md
```

As apps ficam em `backend/apps/` (pacote Python), e os imports devem usar o prefixo `apps.*` (ex.: `apps.usuarios`). As apps já estão registradas em `INSTALLED_APPS` no `backend/escola/settings.py`.

## Execução
```bash
cd backend
python manage.py migrate
python manage.py runserver
```

Após subir, a documentação interativa estará em `/api/docs/` e o schema OpenAPI em `/api/schema/`.

## Seeds de desenvolvimento
Para popular dados básicos (usuários, séries/disciplinas, responsáveis e alunos):
```bash
cd backend
python manage.py seed_minha_escola
```
Usuários criados (senha padrão entre parênteses):
- admin (admin123) — superusuário
- diretoria (senha123)
- coordenacao (senha123)
- secretaria (senha123)
- professor (senha123)

## Comandos sugeridos (exemplos)
Estes são os comandos típicos para criar a estrutura do zero (já aplicados neste repositório):
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate ; Linux/Mac: source .venv/bin/activate
pip install -r backend/requirements.txt

cd backend
django-admin startproject escola .
python manage.py startapp usuarios
python manage.py startapp core
python manage.py startapp academico
python manage.py startapp matriculas
python manage.py startapp financeiro
python manage.py startapp comunicacao
python manage.py startapp documentos

# mover apps para backend/apps e criar __init__.py
```

Observações:
- Por padrão, o `settings.py` usa SQLite para desenvolvimento. Para usar MySQL, defina `DB_ENGINE=mysql` e variáveis `MYSQL_*` no `.env`.
- CORS está liberado em `DEBUG`. Em produção, configure `CORS_ALLOWED_ORIGINS` e `ALLOWED_HOSTS`.
- Autenticação padrão via SimpleJWT já configurada no DRF.

## Arquitetura (visão geral)
```
Frontend (Angular)
   │  HTTP (JWT)
   ▼
Backend API (Django + DRF)
   │  ORM
   ▼
Banco de Dados (MySQL)
```

Componentes principais:
- Auth: SimpleJWT (`/api/auth/token`, `/api/auth/refresh`)
- Core: Alunos, Responsáveis, Endereços (`/api/core/...`)
- Acadêmico: Séries, Disciplinas, Turmas, Aulas, Avaliações, Notas (`/api/academico/...`)
- Matrículas: Planos, Propostas, Matrículas (`/api/matriculas/...`)
- Financeiro: Faturas e Baixas (`/api/financeiro/...`)
- Documentos: PDFs (Boletim, Declaração) (`/api/documentos/...`)

## Fluxos
1) Matrícula
- Criar uma `PropostaMatricula` para um aluno.
- Aprovar proposta informando `turma`, `plano` e `ano_letivo` → cria/ativa `Matricula`.

2) Geração de Faturas
- Dado uma `Matricula`, gerar faturas mensais (parcelas) a partir de um mês base.
- Cada fatura possui `competencia`, `vencimento`, `valor`, `status`.

3) Baixa (Pagamento)
- Registrar `Baixa` em uma `Fatura` (data/valor/observação) → status da fatura vai para `PAGA`.

## Perfis e Permissões
- Tipos de usuário (`apps.usuarios.models.Tipo`):
  - DIRETORIA, COORDENACAO, SECRETARIA, PROFESSOR, RESPONSAVEL, ALUNO
- Regras principais:
  - Apenas `DIRETORIA` e `COORDENACAO` podem realizar CRUD de usuários (endpoint `/api/usuarios/usuarios/`).
  - Demais recursos exigem autenticação (`IsAuthenticated`). Regras mais finas podem ser adicionadas conforme necessidade.
  - Listagens padronizadas retornam registros ativos (deleção lógica via campo `ativo/ativa`).

## Exemplos de requisições (curl)

Autenticação (Obter Token):
```bash
curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
# resposta: {"access":"<JWT>", "refresh":"<JWT>"}
```

Exportar token para uso nos próximos comandos:
```bash
TOKEN=<COLE_AQUI_O_ACCESS>
```

Alunos (CRUD básico):
```bash
# Listar
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/core/alunos/

# Criar
curl -X POST http://localhost:8000/api/core/alunos/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"nome":"Novo Aluno","matricula":"A1234","cpf":"000.000.000-99"}'

# Detalhar
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/core/alunos/1/

# Atualizar
curl -X PATCH http://localhost:8000/api/core/alunos/1/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"ativo":false}'

# Excluir (físico). Como padrão listamos apenas ativos.
curl -X DELETE -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/core/alunos/1/
```

Propostas/Matrículas:
```bash
# Criar proposta
curl -X POST http://localhost:8000/api/matriculas/propostas/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"aluno":1, "observacao":"Matrícula 2025"}'

# Aprovar proposta (gera/atualiza matrícula)
curl -X POST http://localhost:8000/api/matriculas/propostas/10/aprovar_proposta/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"turma":2, "plano":1, "ano_letivo":2025}'
```

Financeiro:
```bash
# Gerar faturas para a matrícula 5 (12 parcelas a partir de 2025-01-01)
curl -X POST "http://localhost:8000/api/financeiro/faturas/gerar_para_matricula/5?parcelas=12&mes_base=2025-01-01" \
  -H "Authorization: Bearer $TOKEN"

# Listar faturas em aberto da matrícula 5
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/financeiro/faturas/?matricula=5&status=ABERTA"

# Baixar fatura 20
curl -X POST http://localhost:8000/api/financeiro/faturas/20/baixar/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"data_pagamento":"2025-02-05","valor_pago":"500.00","observacao":"PIX"}'
```

Documentos (PDF):
```bash
# Boletim do aluno 1 (ano atual)
curl -H "Authorization: Bearer $TOKEN" -H "Accept: application/pdf" \
  -o boletim-1.pdf http://localhost:8000/api/documentos/boletim/1/

# Declaração de matrícula
curl -H "Authorization: Bearer $TOKEN" -H "Accept: application/pdf" \
  -o declaracao-1.pdf http://localhost:8000/api/documentos/declaracao_matricula/1/
```

## Frontend (Angular)
Criação do projeto e dependências:
```bash
cd frontend
ng new minha-escola-app --routing --style=scss
cd minha-escola-app
npm i @auth0/angular-jwt @angular/material @angular/forms @angular/cdk ngx-toastr dayjs
```

Interceptor JWT
- Arquivo: `frontend/minha-escola-app/src/app/core/interceptors/jwt.interceptor.ts`
- Registro em `src/app/app.module.ts`:
```ts
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { JwtInterceptor } from './core/interceptors/jwt.interceptor';

@NgModule({
  // ...
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
  ],
})
export class AppModule {}
```

## Como rodar (Backend)
Passo a passo para subir o backend em desenvolvimento:
```bash
# 1) Copiar o arquivo de ambiente e preencher as variáveis
# Windows (PowerShell): Copy-Item backend/.env.example backend/.env
# Linux/Mac: cp backend/.env.example backend/.env

# 2) Escolher o banco
# - Para começar rápido, deixe DB_ENGINE=sqlite no backend/.env
# - Para usar MySQL, mude para DB_ENGINE=mysql e preencha DB_*

# 3) Aplicar migrações
cd backend
python manage.py makemigrations
python manage.py migrate

# 4) Criar superusuário
python manage.py createsuperuser

# 5) Popular dados de exemplo (opcional)
python manage.py seed_minha_escola

# 6) Executar o servidor
python manage.py runserver 8000
```

### Notas sobre MySQL no Windows
- Se optar por MySQL e usar `mysqlclient`, você precisará do Microsoft C++ Build Tools e do Connector/C (ou equivalentes) para compilar o pacote.
- Alternativas:
  - Use SQLite no desenvolvimento (DB_ENGINE=sqlite) e mantenha MySQL apenas em produção.
  - Instale um conector puro Python (ex.: PyMySQL) e configure `pymysql.install_as_MySQLdb()` (posso ajustar o projeto se preferir).
