#Rotas para laboratórios
from flask import Blueprint, render_template, request, redirect, url_for
from ..models.laboratorios import Lab, ReservaLab
from ..database import *
lab_bp = Blueprint(name ='lab', 
                    import_name= __name__, 
                    url_prefix='/lab', 
                    template_folder='templates')

@lab_bp.route('/')
def index():
    return 'laboratorios'

@lab_bp.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar_lab():
    if request.method == 'POST':
        nome_lab = request.form['nome_lab']
        especialidade_lab = request.form['especialidade_lab']
        local_lab = request.form['local_lab']
        capacidade_lab = request.form['capacidade_lab']
        laboratorio = Lab(nome_lab, especialidade_lab, local_lab, capacidade_lab)
        return f"<h1> metodo post nome: {nome_lab} especialidade: {especialidade_lab} local: {local_lab} quantidade: {capacidade_lab}</h1>"
    return render_template('laboratorios/cadastrar_lab.html')