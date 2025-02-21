#Rotas para laboratórios
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from ..models.laboratorios import Lab, ReservaLab
from ..database import db
from ..decorators.auth import role_required
from datetime import datetime
lab_bp = Blueprint(name ='lab', 
                    import_name= __name__, 
                    url_prefix='/lab', 
                    template_folder='templates')

@lab_bp.route('/')
def index():
    laboratorios = db.session.scalars(db.select(Lab)).all()
    return f'{laboratorios}'

@lab_bp.route('/reservas')
def reservas():
    reservas = db.session.scalars(db.select(ReservaLab)).all()
    return f'{reservas}'


@lab_bp.route('/cadastrar', methods=['POST', 'GET'])
# @role_required('Técnico')
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


@lab_bp.route('/reservar', methods = ['GET', 'POST'])
def reservar_lab():
    if request.method == 'POST':
        nome_lab = request.form['nome_lab']
        lab_id = db.session.scalar(db.select(Lab.lab_id).filter(Lab.lab_nome == nome_lab))
        tipo_reserva = request.form['tipo_reserva']
        motivo_reserva = request.form['motivo_reserva']
        horario_inicio = datetime.strptime(request.form['horario_inicio'], '%H:%M').time()
        horario_termino = datetime.strptime(request.form['horario_termino'], '%H:%M').time()
        data_inicio = datetime.strptime(request.form['data_inicio'], '%Y-%m-%d').date()
        if tipo_reserva == 'extraordinaria':
            data_final = data_inicio
        else:
            data_final = datetime.strptime(request.form['data_final'], '%Y-%m-%d').date()


        reserva_existente = db.session.scalar(db.select(ReservaLab).filter(ReservaLab.rel_lab_id == lab_id, ReservaLab.rel_dataFinal >= data_inicio, ReservaLab.rel_dataInicial <= data_final, ReservaLab.rel_horarioFinal >= horario_inicio, ReservaLab.rel_horarioInicial <= horario_termino))
        if reserva_existente:
            flash("Já existe uma reserva para esse período!", "danger")
            print("Já existe uma reserva para esse período!")
            return redirect(url_for('lab.reservar_lab'))
        else:
            reserva = ReservaLab(data_inicio, data_final, horario_inicio, horario_termino, motivo_reserva, tipo_reserva, lab_id, current_user.usu_matricula)
            db.session.add(reserva)
            db.session.commit()
            flash('solicitação de reserva de laboratório realizada!')
            return redirect(url_for('lab.reservas'))
    
    return render_template('laboratorios/reservar_lab.html')