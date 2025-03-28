from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, logout_user, login_required, current_user

from sqlalchemy.exc import OperationalError
import time
import pymysql
from database import db
from auth import auth_bp
from models.usuarios import User
from models.laboratorios import Lab, ReservaLab, EspecialidadeLab
from models.materiais import Material, ReservaMaterial, Categoria, Reagente
from controllers import lab_bp, materiais_bp, usu_bp

pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultramegadificil'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/db_labstock'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://lab:stock@db/labstock'

#login_manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

#registrar os bps
app.register_blueprint(lab_bp)
app.register_blueprint(materiais_bp)
app.register_blueprint(usu_bp)
app.register_blueprint(auth_bp)

db.init_app(app)

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
        return render_template('pages/inicioProfessor.html', nome = usuario.usu_nome)
    elif usuario.usu_tipo == 'Técnico':
        return render_template('pages/inicioTecnico.html', nome = usuario.usu_nome)
    else:
        return render_template('pages/inicio.html', nome = usuario.usu_nome)

@app.route('/sobre')
def sobre():
    return render_template('pages/sobre.html')


@app.route('/laboratorios')
def laboratorios():
    return render_template('pages/laboratorios.html')


# @app.route('/reservar')
# def reservar():
#     return render_template('pages/reserva')


@app.route('/profdash')
def visualizar_prof():
    return render_template('pages/inicioProfessor.html')


@app.route('/tecdash')
def visualizar_aluno():
    return render_template('pages/inicioTecnico.html')



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3000, debug=True)

