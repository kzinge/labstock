from ... import aulas_bp
from flask import render_template, request, redirect, url_for, flash
from ..services import aulaservice
from flask_login import current_user
from ....laboratorio.actions.services import labservice

@aulas_bp.route('/')
def index():
    aulas = aulaservice.get_aulas()
    return render_template('aulas/view.html', aulas=aulas)

@aulas_bp.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar_aula():
    if request.method == 'POST':
        aulaservice.cadastrar_aula(request.form)
        return redirect(url_for('aulas.index'))
    else:
        labs = labservice.carregar_labs()
        return render_template('aulas/cadastrar_aula.html',labs=labs)