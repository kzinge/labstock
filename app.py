from flask import Flask, render_template, redirect, url_for

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

#teste de commit