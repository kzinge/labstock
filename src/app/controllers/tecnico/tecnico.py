#Rotas para técnicos
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from ...database import db
from ...models import User

tec_bp = Blueprint(name ='tecnico', 
                    import_name= __name__, 
                    url_prefix='/tecnico', 
                    template_folder='pages')

@tec_bp.route('/')
def home():
    return 'teste'

@tec_bp.route('/categorias', methods=['POST','GET'])
def cadastrar_categoria():
    if request.method == 'GET':
        return render_template('/pages/categoria.html')
    else:
    
        materialservice.nova_categoria(request.form)
        flash('Categoria criada com sucesso!')
        return redirect(url_for('tecnico.cadatrar_categoria'))