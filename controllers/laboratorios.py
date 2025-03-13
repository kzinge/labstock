#Rotas para laboratórios
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from models.laboratorios import Lab, ReservaLab, EspecialidadeLab
from database import db
from decorators.auth import role_required
from datetime import datetime
lab_bp = Blueprint(name ='lab', 
                    import_name= __name__, 
                    url_prefix='/lab', 
                    template_folder='templates')

@lab_bp.route('/')
def index():
    laboratorios = db.session.scalars(db.select(Lab)).all()
    return render_template('laboratorios/view_lab.html', laboratorios = laboratorios)



@lab_bp.route('/cadastrar', methods=['POST', 'GET'])
# @role_required('Técnico')
def cadastrar_lab():
    especialidades = db.session.scalars(db.select(EspecialidadeLab)).all()
    print(especialidades)
    if not especialidades: #cria a especialidade química se n houver nenhuma
        especialidade = EspecialidadeLab(esp_nome = "Química")
        db.session.add(especialidade)
        db.session.commit()
        print("cadastrou uma especialidade")

    elif request.method == 'POST':
        nome_lab = request.form['nome_lab']
        especialidade_lab = request.form['especialidade_lab']
        local_lab = request.form['local_lab']
        capacidade_lab = request.form['capacidade_lab']
        laboratorio = Lab(nome_lab, local_lab, capacidade_lab, especialidade_lab)
        db.session.add(laboratorio)
        db.session.commit()
        flash('cadastro de laboratório realizado!')
        return redirect(url_for('lab.index'))
    especialidades = db.session.scalars(db.select(EspecialidadeLab)).all()
    return render_template('laboratorios/cadastrar_lab.html', especialidades=especialidades)

@lab_bp.route('/reservas')
def reservas():
    reservas = db.session.scalars(db.select(ReservaLab)).all()
    return render_template('laboratorios/view_reservas.html', reservas = reservas)

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
    laboratorios = db.session.scalars(db.select(Lab)).all()
    return render_template('laboratorios/reservar_lab.html', laboratorios = laboratorios)

@lab_bp.route('/editar_reserva/<int:reserva_id>', methods=['GET', 'POST'])
def editar_reserva(reserva_id):
    reserva = db.session.get(ReservaLab, reserva_id) 
    if not reserva:
        flash("Reserva não encontrada!", "danger")
        return redirect(url_for('lab.reservas'))

    if request.method == 'POST':
        reserva.rel_lab_id = db.session.scalar(db.select(Lab.lab_id).filter(Lab.lab_nome == request.form['nome_lab']))
        reserva.rel_tipo = request.form['tipo_reserva']
        reserva.rel_motivo = request.form['motivo_reserva']
        reserva.rel_horarioInicial = datetime.strptime(request.form['horario_inicio'], '%H:%M').time()
        reserva.rel_horarioFinal = datetime.strptime(request.form['horario_termino'], '%H:%M').time()
        reserva.rel_dataInicial = datetime.strptime(request.form['data_inicio'], '%Y-%m-%d').date()
        if request.form['tipo_reserva'] == 'extraordinaria':
            reserva.rel_dataFinal = reserva.rel_dataInicial
        else:
            reserva.rel_dataFinal = datetime.strptime(request.form['data_final'], '%Y-%m-%d').date()

        db.session.commit()
        flash('Reserva atualizada com sucesso!', 'success')
        return redirect(url_for('lab.reservas'))

    laboratorios = db.session.scalars(db.select(Lab)).all()
    return render_template('laboratorios/editar_reserva.html', reserva=reserva, laboratorios=laboratorios)


@lab_bp.route('/excluir_reserva/<int:reserva_id>', methods=['POST'])
def excluir_reserva(reserva_id):
    reserva = db.session.get(ReservaLab, reserva_id)  
    if not reserva:
        flash("Reserva não encontrada!", "danger")
        return redirect(url_for('lab.reservas'))

    db.session.delete(reserva)
    db.session.commit()
    flash('Reserva excluída com sucesso!', 'success')
    return redirect(url_for('lab.reservas'))

@lab_bp.route('/confirmar_reserva/<int:reserva_id>', methods=['POST'])
def confirmar_reserva(reserva_id):
    reserva = db.session.get(ReservaLab, reserva_id)
    if not reserva:
        flash("Reserva não encontrada!", "danger")
        return redirect(url_for('lab.reservas'))

    reserva.rel_status = 'Confirmada'
    db.session.commit()
    flash('Reserva confirmada com sucesso!', 'success')
    return redirect(url_for('lab.reservas'))

@lab_bp.route('/rejeitar_reserva/<int:reserva_id>', methods=['POST'])
def rejeitar_reserva(reserva_id):
    reserva = db.session.get(ReservaLab, reserva_id)
    if not reserva:
        flash("Reserva não encontrada!", "danger")
        return redirect(url_for('lab.reservas'))

    reserva.rel_status = 'Rejeitada'
    db.session.commit()
    flash('Reserva rejeitada com sucesso!', 'success')
    return redirect(url_for('lab.reservas'))