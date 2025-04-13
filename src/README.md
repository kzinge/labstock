# Diretório `src`

Este diretório contém todo o código-fonte principal da aplicação. A estrutura é organizada para manter **separação de responsabilidades**, facilitar a **manutenção** e permitir **escalabilidade**.

---

## Estrutura
src
└── app
    ├── api
    ├── auth
    │   └── utils
    ├── controllers
    │   ├── aluno
    │   │   ├── actions
    │   │   │   ├── routes
    │   │   │   └── services
    │   │   └── views
    │   ├── laboratorio
    │   │   ├── actions
    │   │   │   ├── routes
    │   │   │   └── services
    │   │   └── views
    │   ├── material
    │   │   ├── actions
    │   │   │   ├── routes
    │   │   │   └── services
    │   │   └── views
    │   ├── professor
    │   │   ├── actions
    │   │   │   ├── routes
    │   │   │   └── services
    │   │   └── views
    │   └── tecnico
    │       ├── actions
    │       │   ├── routes
    │       │   └── services
    │       └── views
    ├── database
    ├── decorators
    ├── models
    ├── static
    │   ├── assets
    │   │   └── devs
    │   ├── css
    │   │   ├── laboratorios
    │   │   ├── materiais
    │   │   └── pages
    │   └── scripts
    └── templates
        ├── laboratorios
        ├── materiais
        └── pages
            └── professor
    ├── __init__.py
    ├── config.py
---

## Descrição dos diretórios

- **api/**  
  *(Futuro uso ou integrações externas)*  
  Arquivos relacionados a APIs externas ou interfaces específicas. Pode ser usado para organização de endpoints públicos ou comunicação com outros sistemas.

- **auth/**  
  Responsável pelo controle de autenticação e autorização dos usuários, como login, logout e utilitários de segurança.

- **controllers/**  
  Diretório que concentra a lógica de negócio. Cada entidade importante do sistema (aluno, laboratório, material, professor, técnico) possui:
  
  - `actions/`  
    - `routes/`: define as rotas específicas daquele módulo.
    - `services/`: regras de negócio, processamento e validação.
  
  - `views/`: renderiza os templates relacionados a cada entidade.

- **database/**  
  Configuração de conexão com o banco de dados, além da inicialização de tabelas e sessões.

- **decorators/**  
  Decorators customizados usados para autenticação, verificação de permissões e controle de acesso.

- **models/**  
  Contém os modelos de dados da aplicação, geralmente definidos via SQLAlchemy ou outro ORM.

- **static/**  
  Arquivos estáticos do frontend:  
  - `assets/`: imagens, ícones, logos etc.
  - `css/`: folhas de estilo organizadas por domínio da aplicação.
  - `scripts/`: JavaScript personalizado para interação no frontend.

- **templates/**  
  Arquivos de template `Jinja2` para renderização de páginas web.
  - `laboratorios/`: páginas relacionadas aos laboratórios.
  - `materiais/`: páginas de gerenciamento de materiais.
  - `pages/`: demais páginas gerais do projeto.

---

## Inicialização da Aplicação (`__init__.py` e `config.py`)

O arquivo `__init__.py` localizado dentro do pacote `src/app/` é responsável por inicializar toda a aplicação Flask, incluindo:

- configuração de banco de dados;
- inicialização de extensões como o `LoginManager`;
- registro dos **blueprints**;
- criação automática do banco de dados se ele ainda não existir;
- definição de rotas globais.

---

## 💡 Arquivo `__init__.py`

### O que ele faz?

Este arquivo é o **coração da aplicação Flask**. Ele é responsável por:

- Configurar variáveis sensíveis e ambiente;
- Conectar ao banco de dados MySQL;
- Preparar e gerenciar autenticação com `Flask-Login`;
- Registrar blueprints;
- Criar tabelas no banco de dados se necessário;
- Definir rotas principais da aplicação.

---

### 🔍 Componentes principais

- **Variáveis de Ambiente**
    ```python
    load_dotenv('.env')
    ```
    Carrega configurações externas, como senhas e URLs, de forma segura.

- **Configuração do Banco de Dados**
    ```python
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{mysqlsenha}@localhost/db_labstock'
    ```
    Permite alternar facilmente entre conexão local ou Docker, bastando comentar/descomentar as opções.

- **Gerenciamento de Usuário**
    ```python
    login_manager = LoginManager()
    login_manager.init_app(app)
    ```
    Integra o Flask com `LoginManager` para autenticação.

- **Registro de Blueprints**
    ```python
    app.register_blueprint(lab_bp)
    app.register_blueprint(materiais_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(prof_bp)
    app.register_blueprint(tec_bp)
    ```
    Os blueprints organizam as rotas de maneira modular por domínio: `laboratorio`, `material`, `professor`, `tecnico` e `auth`.

- **Conexão ao Banco de Dados com Tolerância**
    ```python
    while not connected:
        try:
            db.create_all()
            connected = True
        except OperationalError:
            time.sleep(2)
    ```
    Essa abordagem garante que o serviço Flask só funcione após o banco de dados estar pronto, muito útil em ambientes Docker.

- **Rotas Globais**
    Define as rotas principais da aplicação, como:
    - `/` — Página de login ou redirecionamento.
    - `/inicio` — Dashboard pós-login baseado no tipo de usuário.
    - `/sobre` — Página informativa.

---

## ⚙️ `config.py`

### O que ele faz?

Este arquivo fornece uma função utilitária muito prática:

- **find_free_port(start_port)**  
  Verifica se uma porta está disponível a partir do número informado e retorna a primeira porta livre.  

Exemplo:
```python
port = find_free_port(5000)