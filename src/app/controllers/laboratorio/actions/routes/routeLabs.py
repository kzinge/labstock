from flask import render_template, request, redirect, url_for, flash
from ... import lab_bp
from ..services import labservice

@lab_bp.route('/')
def index():
    laboratorios = labservice.carregar_labs()
    return render_template('laboratorios/view_lab.html', laboratorios = laboratorios)

@lab_bp.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar_lab():
    labservice.verificar_especialidade()

    if request.method == 'POST':
        sucesso, mensagem = labservice.cadastrar_lab(request.form)
        flash(mensagem, 'success' if sucesso else 'danger')
        if sucesso:
            return redirect(url_for('lab.index'))

    especialidades = labservice.listar_especialidades()
    return render_template('laboratorios/cadastrar_lab.html', especialidades=especialidades)

@lab_bp.route('/reservas', methods=['GET', 'POST'])
def reservas():
    if request.method == 'POST':
        reservas = labservice.filtrar_labs(request.form)
    elif request.method == 'GET':
        reservas = labservice.carregar_reservas()
    especialidades = labservice.listar_especialidades()
    return render_template('laboratorios/view_reservas.html', reservas = reservas, especialidades = especialidades)

@lab_bp.route('/reservar', methods=['GET', 'POST'])
def reservar_lab():
    if request.method == 'POST':
        return labservice.reservar(request.form)

    laboratorios = labservice.carregar_labs()
    return render_template('laboratorios/reservar_lab.html', laboratorios=laboratorios)

@lab_bp.route('/editar_reserva/<int:reserva_id>', methods=['GET', 'POST'])
def editar_reserva(reserva_id):
    if request.method == 'POST':
        return labservice.atualizar_reserva(reserva_id, request.form)

    reserva = labservice.carregar_reserva(reserva_id)
    if not reserva:
        flash("Reserva não encontrada!", "danger")
        return redirect(url_for('lab.reservas'))

    laboratorios = labservice.carregar_labs()
    return render_template('laboratorios/editar_reserva.html', reserva=reserva, laboratorios=laboratorios)

@lab_bp.route('/excluir_reserva/<int:reserva_id>', methods=['POST'])
def excluir_reserva(reserva_id):
    return labservice.excluir_reserva(reserva_id)

@lab_bp.route('/confirmar_reserva/<int:reserva_id>', methods=['POST'])
def confirmar_reserva(reserva_id):
    return labservice.atualizar_status_reserva(reserva_id, 'Confirmada')

@lab_bp.route('/rejeitar_reserva/<int:reserva_id>', methods=['POST'])
def rejeitar_reserva(reserva_id):
    return labservice.atualizar_status_reserva(reserva_id, 'Indeferida')

@lab_bp.route('/detalhar_reserva/<int:reserva_id>')
def detalhar_reserva(reserva_id):
    return labservice.detalhar_reserva(reserva_id)