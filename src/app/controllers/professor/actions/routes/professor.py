from ... import prof_bp
from ..services.user import find_user
from flask import render_template, redirect, url_for

@prof_bp.route('/')
def home():
    usuario = find_user()
    return render_template('home.html', nome = usuario.usu_nome)
