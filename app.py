from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, logout_user, login_required, current_user
from os import getenv
from dotenv import load_dotenv
from .database import db
from .auth import auth_bp
from .models.usuarios import User
from .models.laboratorios import Lab, ReservaLab
from .models.materiais import Material, ReservaMaterial, Categoria
from .controllers import lab_bp, materiais_bp, usu_bp

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
app.register_blueprint(materiais_bp)
app.register_blueprint(usu_bp)
app.register_blueprint(auth_bp)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard') )
    return render_template('pages/index.html')


@app.route('/inicio')
@login_required
def dashboard():
    usuario = db.session.scalar(db.select(User).where(User.usu_matricula == current_user.usu_matricula))
    return render_template('pages/inicio.html', nome = usuario.usu_nome, foto = usuario.usu_foto, tipo = usuario.usu_tipo)

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



if __name__ == '__main__':
    app.run(host='10.146.6.4', port=5000)