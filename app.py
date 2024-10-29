from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('pages/index.html')


@app.route('/inicio')
def dashboard():
    return render_template('pages/inicio.html')


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


@app.route('/cadastrar_material', methods=['POST', 'GET'])
def cadastrar_material():
    if request.method == 'POST':
        nome_material = request.form['nome_material']
        tipo_material = request.form['tipo_material']
        return f"<h1> metodo post nome: {nome_material} tipo: {tipo_material}</h1>"
    return render_template('pages/cadastrar_material.html')


@app.route('/cadastrar_lab', methods=['POST', 'GET'])
def cadastrar_lab():
    if request.method == 'POST':
        nome_lab = request.form['nome_lab']
        especialidade_lab = request.form['especialidade_lab']
        local_lab = request.form['local_lab']
        capacidade_lab = request.form['capacidade_lab']
        return f"<h1> metodo post nome: {nome_lab} especialidade: {especialidade_lab} local: {local_lab} quantidade: {capacidade_lab}</h1>"
    return render_template('pages/cadastrar_lab.html')