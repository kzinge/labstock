# 💻 Sistema de Gestão de Laboratórios

Bem-vindo!  
Este é um sistema de gerenciamento de reservas e controle de materiais para laboratórios acadêmicos. O projeto foi desenvolvido utilizando Python, Flask e MySQL, com deploy simplificado via Docker.

---

## 🚀 Funcionalidades

- ✅ Autenticação via SUAP de usuários (Professor, Técnico, Aluno).
- 🗓️ Gerenciamento de reservas de laboratórios.
- 📦 Controle de entrada e saída de materiais.
- 🔒 Sistema de login com Flask-Login.
- 🐳 Suporte a Docker e Docker Compose.
- 🔥 Organização de rotas com Blueprints.
- 💡 Separação clara entre lógicas de `service`, `routes` e `views`.

---

## 🗂️ Estrutura do Projeto

```
docker/
├── docker-compose.yml
├── dockerfile
├── DockerTutorial.md
└── nginx/
    └── default.conf

src/
└── app/
    ├── api/
    ├── auth/
    ├── controllers/
    ├── database/
    ├── decorators/
    ├── models/
    ├── static/
    └── templates/
```

- `docker/`: Arquivos para build e deploy via Docker.
- `src/app/`: Código-fonte principal da aplicação.
- `controllers/`: Camada que organiza as ações, rotas e visualizações de cada módulo.
- `auth/`: Controle de autenticação e segurança.
- `models/`: Classes que representam as tabelas no banco de dados.
- `database/`: Configuração da conexão com o MySQL.
- `static/` e `templates/`: Arquivos estáticos e templates Jinja2.

---

## ⚙️ Configuração

### Pré-requisitos

- Python 3.11+
- MySQL Server
- Docker (opcional para deploy)

### 📌 Setup Local

1. Clone o repositório:
    ```bash
    git clone https://github.com/seuusuario/labstock.git
    cd labstock
    ```

2. Crie o arquivo `.env` com suas variáveis:
    ```
    MYSQL_PASS=sua_senha
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Execute a aplicação:
    ```bash
    python run.py
    ```

---

### 🐳 Deploy com Docker

1. Configure o `.env` e o `docker-compose.yml`.
2. Suba os containers:
    ```bash
    docker compose up --build
    ```

O NGINX vai gerenciar o acesso, o banco MySQL será inicializado e a aplicação Flask estará rodando.

---

## 🧐 Design de Software

O projeto segue uma estrutura clara e modular:

- `actions/` → Lógica de negócios (services e rotas organizados).
- `views/` → Templates HTML.
- `models/` → ORM SQLAlchemy.
- `decorators/` → Funções auxiliares e middlewares.
- `auth/` → Login, logout e controle de sessões.

---
