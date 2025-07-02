from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import pymysql
from os import getenv
from sqlalchemy.exc import OperationalError
import time
from .database import db
from .auth import auth_bp
from .models.usuarios import User

# Importando blueprints
from .controllers.laboratorio import lab_bp
from .controllers.material import materiais_bp
from .controllers.professor import prof_bp
from .controllers.tecnico import tec_bp
from .controllers.aulas import aulas_bp

load_dotenv('.env')

mysqlsenha = getenv('MYSQL_PASS')

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultramegadificil'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{mysqlsenha}@localhost/db_labstock'
# Para Docker: descomente abaixo quando necessário
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://lab:stock@db/labstock'

# Configuração do login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

# Registrar os blueprints
app.register_blueprint(lab_bp)
app.register_blueprint(materiais_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(prof_bp)
app.register_blueprint(tec_bp)
app.register_blueprint(aulas_bp)

db.init_app(app)

# Conexão com o banco de dados
with app.app_context():
    connected = False
    while not connected:
        try:
            db.create_all()
            connected = True
            print("✅ Conexão com o banco de dados estabelecida!")
        except OperationalError:
            print("⏳ Banco de dados ainda não está pronto. Tentando novamente em 2 segundos...")
            time.sleep(2)

# Definindo as rotas
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard') )
    return render_template('pages/index.html')

@app.route('/inicio')
@login_required
def dashboard():
    usuario = db.session.scalar(db.select(User).where(User.usu_matricula == current_user.usu_matricula))
    if usuario.usu_tipo == 'Docente':
        return redirect(url_for('professor.home'))
    elif usuario.usu_tipo == 'Técnico':
        return render_template('pages/inicioTecnico.html', nome = usuario.usu_nome)
    else:
        return render_template('pages/inicio.html', nome = usuario.usu_nome)

@app.route('/sobre')
def sobre():
    return render_template('pages/sobre.html')

@app.route('/laboratorios')
def laboratorios():
    pass

@app.route('/profdash')
def visualizar_prof():
    return render_template('pages/inicioProfessor.html')


