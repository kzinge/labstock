from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/inicio')
def dashboard():
    return render_template('pages/inicio.html')