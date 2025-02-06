#Rotas para laboratórios
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.laboratorios import Lab, ReservaLab
from ..database import db
lab_bp = Blueprint(name ='lab', 
                    import_name= __name__, 
                    url_prefix='/lab', 
                    template_folder='templates')

@lab_bp.route('/')
def index():
    laboratorios = db.session.scalars(db.select(Lab)).all()
    return f'{laboratorios}'

@lab_bp.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar_lab():
    if request.method == 'POST':
        nome_lab = request.form['nome_lab']
        especialidade_lab = request.form['especialidade_lab']
        local_lab = request.form['local_lab']
        capacidade_lab = request.form['capacidade_lab']
        laboratorio = Lab(nome_lab, especialidade_lab, local_lab, capacidade_lab)
        db.session.add(laboratorio)
        db.session.commit()
        flash('cadastro de laboratório realizado!')
        return redirect(url_for('lab.index'))
    return render_template('laboratorios/cadastrar_lab.html')