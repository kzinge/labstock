from flask import redirect,render_template, request, flash, url_for
from flask_login import current_user
from .....models import Lab, ReservaLab, EspecialidadeLab
from .....database import db
from .....decorators.auth import role_required
from datetime import datetime, date

def carregar_labs():
    laboratorios = db.session.scalars(db.select(Lab)).all()
    
    return laboratorios

def numero_reservas(lab_id):
    count = db.session.scalar(db.select(db.func.count()).filter(ReservaLab.rel_lab_id == lab_id))
    return count

def cadastrar_lab(form):
    try:
        nome_lab = form['nome']
        bloco_lab = form['bloco']
        sala_lab = form['sala'].upper()
        capacidade_lab = form['capacidade']
        especialidade_lab = form['especialidade']

        laboratorio = Lab(nome_lab, bloco_lab, sala_lab, capacidade_lab, especialidade_lab)
        db.session.add(laboratorio)
        db.session.commit()

        return True, "Cadastro de laboratório realizado com sucesso!"
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao cadastrar laboratório: {e}")
        return False, f"Erro ao cadastrar laboratório: {e}"

#Especialidade
def verificar_especialidade():
    especialidades = db.session.scalars(db.select(EspecialidadeLab)).all()
    if not especialidades:
        especialidade = EspecialidadeLab(esp_nome="Química")
        db.session.add(especialidade)
        db.session.commit()
        return True  # criou uma nova
    return False  # já existia

def listar_especialidades():
    return db.session.scalars(db.select(EspecialidadeLab)).all()

def carregar_reservas():
    reservas = db.session.scalars(db.select(ReservaLab)).all()
    return reservas

def carregar_reservas_pendentes():
    reservas_pendentes = db.session.query(ReservaLab).filter(ReservaLab.rel_status == 'Pendente').all()
    return reservas_pendentes

def minhas_reservas():
    reservas = db.session.query(ReservaLab).filter(ReservaLab.rel_usu_matricula == current_user.usu_matricula).all()
    return reservas

def minhas_reservas_pendentes():
    reservas_pendentes = db.session.query(ReservaLab).filter(ReservaLab.rel_status == 'Pendente', ReservaLab.rel_usu_matricula == current_user.usu_matricula).all()
    return reservas_pendentes

def filtrar_labs(form):
    filtro_especialidade = form.get('especialidades_filtro')
    filtro_nome = form.get('buscar_lab')
    filtro_data = form.get('data_filtro')
    filtro_hora = form.get('horario_filtro')

    query = db.select(Lab)

    # Filtro de especialidade
    if filtro_especialidade != 'todas':
        esp_id = db.session.scalar(
            db.select(EspecialidadeLab.esp_id).filter(EspecialidadeLab.esp_nome == filtro_especialidade)
        )
        if esp_id:
            query = query.filter(Lab.lab_especialidade == esp_id)

    # Filtro de nome
    if filtro_nome:
        query = query.filter(Lab.lab_nome.ilike(f"%{filtro_nome}%"))

    # Filtro de disponibilidade em data e hora
    if filtro_data and filtro_hora:
        subquery = db.select(ReservaLab.rel_lab_id).filter(
            db.func.date(ReservaLab.rel_horarioInicial) == filtro_data,
            db.func.time(ReservaLab.rel_horarioInicial) <= filtro_hora,
            db.func.time(ReservaLab.rel_horarioFinal) >= filtro_hora
        ).subquery()

        query = query.filter(~Lab.lab_id.in_(subquery))  # Exclui os laboratórios que já estão ocupados nesse horário

    laboratorios_disponiveis = db.session.scalars(query).all()
    return laboratorios_disponiveis



def carregar_reserva(reserva_id):
    reserva = db.session.get(ReservaLab, reserva_id)

    return reserva

def reservar(form):
    nome_lab = request.form['nome_lab']
    lab_id = db.session.scalar(db.select(Lab.lab_id).filter(Lab.lab_nome == nome_lab))
    # tipo_reserva = request.form['tipo_reserva']
    motivo_reserva = request.form['motivo_reserva']
    horario_inicio = datetime.strptime(request.form['horario_inicio'], '%H:%M').time()
    horario_termino = datetime.strptime(request.form['horario_termino'], '%H:%M').time()
    data_inicio = datetime.strptime(request.form['data_inicio'], '%Y-%m-%d').date()
    data_hoje = datetime.now().date()
    hora_agora = datetime.now().time()
    if data_inicio < data_hoje or (data_inicio == data_hoje and horario_inicio < hora_agora):
        flash("Você não pode reservar para um horário que já passou!", "danger")
        print("Você não pode reservar para um horário que já passou!", "danger")
        return redirect(url_for('lab.reservar_lab'))
    
    # if tipo_reserva == 'extraordinaria':
    #     data_final = data_inicio
    # else:
    data_final = datetime.strptime(request.form['data_final'], '%Y-%m-%d').date()
    if data_final < data_inicio or horario_termino < horario_inicio:
        print("a data e/ou o horário final não pode ser antes do inicial") 
        flash("a data e/ou o horário final não pode ser antes do inicial") 
        return redirect(url_for('lab.reservar_lab'))
    reserva_existente = db.session.scalar(db.select(ReservaLab).filter(ReservaLab.rel_lab_id == lab_id, ReservaLab.rel_status == 'Confirmada', ReservaLab.rel_dataFinal >= data_inicio, ReservaLab.rel_dataInicial <= data_final, ReservaLab.rel_horarioFinal >= horario_inicio, ReservaLab.rel_horarioInicial <= horario_termino))
    if reserva_existente:
        flash("Já existe uma reserva para esse período!", "danger")
        print("Já existe uma reserva para esse período!")
        return redirect(url_for('lab.reservar_lab'))
    else:
        reserva = ReservaLab(data_inicio, data_final, horario_inicio, horario_termino, motivo_reserva, lab_id, current_user.usu_matricula) #aqui excluí tipo reserva que estava logo dps de motivo
        db.session.add(reserva)
        db.session.commit()
        flash('solicitação de reserva de laboratório realizada!')
        return redirect(url_for('lab.reservas'))
    
def atualizar_reserva(reserva_id, form):

    reserva = carregar_reserva(reserva_id)

    if not reserva:
        flash("Reserva não encontrada!", "danger")
        return redirect(url_for('lab.reservas'))

    reserva.rel_lab_id = db.session.scalar(
        db.select(Lab.lab_id).filter(Lab.lab_nome == form['nome_lab'])
    )
    # reserva.rel_tipo = form['tipo_reserva']
    reserva.rel_motivo = form['motivo_reserva']
    reserva.rel_horarioInicial = datetime.strptime(form['horario_inicio'], '%H:%M').time()
    reserva.rel_horarioFinal = datetime.strptime(form['horario_termino'], '%H:%M').time()
    reserva.rel_dataInicial = datetime.strptime(form['data_inicio'], '%Y-%m-%d').date()

    # if form['tipo_reserva'] == 'extraordinaria':
    #     reserva.rel_dataFinal = reserva.rel_dataInicial
    # else:
    reserva.rel_dataFinal = datetime.strptime(form['data_final'], '%Y-%m-%d').date()

    data_hoje = datetime.now().date()
    hora_agora = datetime.now().time()

    if reserva.rel_dataInicial < data_hoje or (reserva.rel_dataInicial == data_hoje and reserva.rel_horarioInicial < hora_agora):
        flash("Você não pode reservar para um horário que já passou!", "danger")
        return redirect(url_for('lab.editar_reserva', reserva_id=reserva.rel_id))

    if reserva.rel_dataFinal < reserva.rel_dataInicial or reserva.rel_horarioFinal < reserva.rel_horarioInicial:
        flash("A data e/ou o horário final não pode ser antes do inicial!", "danger")
        return redirect(url_for('lab.editar_reserva', reserva_id=reserva.rel_id))

    db.session.commit()
    flash('Reserva atualizada com sucesso!', 'success')
    return redirect(url_for('lab.reservas'))

def excluir_reserva(reserva_id):
    reserva = carregar_reserva(reserva_id)
    if not reserva:
        flash("Reserva não encontrada!", "danger")
        return redirect(url_for('lab.reservas'))

    db.session.delete(reserva)
    db.session.commit()
    flash('Reserva excluída com sucesso!', 'success')
    return redirect(url_for('lab.reservas'))

def atualizar_status_reserva(reserva_id, status):
    reserva = db.session.get(ReservaLab, reserva_id)
    if not reserva:
        flash("Reserva não encontrada!", "danger")
        return redirect(url_for('lab.reservas'))

    reserva.rel_status = status
    db.session.commit()
    flash(f'Reserva {status.lower()} com sucesso!', 'success')
    return redirect(url_for('lab.reservas'))

def detalhar_reserva(reserva_id):
    reserva = carregar_reserva(reserva_id)
    if not reserva:
        flash("Reserva não encontrada!", "danger")
        return redirect(url_for('lab.reservas'))
    return render_template('laboratorios/detalhar_reserva.html', reserva=reserva)