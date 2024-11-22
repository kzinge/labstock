from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, logout_user, login_required, current_user
from os import getenv
from dotenv import load_dotenv
from .database import db
from .auth import auth_bp
from .models.usuarios import User
from .controllers import lab_bp, materias_bp, usu_bp

load_dotenv('.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultramegadificil'
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql://{getenv('MYSQL_USER')}:{getenv('MYSQL_SENHA')}@"
    f"{getenv('MYSQL_HOST')}/{getenv('MYSQL_DB')}"
)

#login_manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

#registrar os bps
app.register_blueprint(lab_bp)
app.register_blueprint(materias_bp)
app.register_blueprint(usu_bp)
app.register_blueprint(auth_bp)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/login')
def login():
    return render_template('pages/login.html')

@login_required
@app.route('/inicio')
def dashboard():
    usuario = db.session.scalar(db.select(User).where(User.usu_id == current_user.usu_id))
    return render_template('pages/inicio.html', nome = usuario.usu_nome)

@app.route('/sobre')
def sobre():
    return render_template('pages/sobre.html')


@app.route('/laboratorios')
def laboratorios():
    return render_template('pages/laboratorios.html')


@app.route('/reserva_materiais')
def reserva_materiais():
    return render_template('pages/reserva_materiais.html')


@app.route('/visualizar_prof')
def visualizar_prof():
    return render_template('pages/visualizar_prof.html')


@app.route('/visualizar_aluno')
def visualizar_aluno():
    return render_template('pages/visualizar_aluno.html')


@app.route('/cadastrar_material', methods=['POST', 'GET'])
def cadastrar_material():
    if request.method == 'POST':
        nome_material = request.form['nome_material']
        tipo_material = request.form['tipo_material']
        return f"<h1> metodo post nome: {nome_material} tipo: {tipo_material}</h1>"
    return render_template('pages/cadastrar_material.html')


@app.route('/cadastrar_lab', methods=['POST', 'GET'])
def cadastrar_lab():
    if request.method == 'POST':
        nome_lab = request.form['nome_lab']
        especialidade_lab = request.form['especialidade_lab']
        local_lab = request.form['local_lab']
        capacidade_lab = request.form['capacidade_lab']
        return f"<h1> metodo post nome: {nome_lab} especialidade: {especialidade_lab} local: {local_lab} quantidade: {capacidade_lab}</h1>"
    return render_template('pages/cadastrar_lab.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso.')
    return redirect(url_for('index'))