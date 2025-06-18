#Rotas para técnicos
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from ...database import db
from ...models import User
from ..material.actions.services import materialservice
from ..laboratorio.actions.services import labservice
from ...models import CategoriaMaterial, CategoriaReagente, EspecialidadeLab

tec_bp = Blueprint(name ='tecnico', 
                    import_name= __name__, 
                    url_prefix='/tecnico', 
                    template_folder='templates/pages')

@tec_bp.route('/')
def index():
    num_labs = len(labservice.carregar_labs())
    num_mats = len(materialservice.get_materiais())
    num_reservas = len(labservice.carregar_reservas())
    return render_template('pages/inicioTecnico.html', num_labs = num_labs, num_mats = num_mats, num_reservas = num_reservas)

def criar_categoria(form):
    if form['tipo'] == "material":
        nome = form['nome_categoria']
        categorias = materialservice.get_categorias_materiais()
        if categorias:
            for categoria in categorias:
                if nome == categoria.cat_nome:
                    flash('Categoria já existe')
                    cat_existente = True

                    return redirect(url_for('material.cadastrar_categoria'))
            if not cat_existente:    
                nova_categoria = CategoriaMaterial(nome)
        else:    
            nova_categoria = CategoriaMaterial(nome)

    elif form['tipo'] == "reagente":
        nome = form['nome_categoria']
        categorias = materialservice.get_categorias_reagentes()
        if categorias:
            for categoria in categorias:
                print('ENTROU NO FOR')
                if nome == categoria.cat_nome:
                    print('CATEGORIA JA EXISTE')
                    flash('Categoria já existe')
                    cat_existente = True

                    return redirect(url_for('material.cadastrar_categoria'))
            if not cat_existente:    
                nova_categoria = CategoriaReagente(form['nome_categoria'])
        else:    
            nova_categoria = CategoriaReagente(form['nome_categoria'])
        
    elif form['tipo'] == "lab":
        nome = form["nome_categoria"]
        categorias = labservice.listar_especialidades()
        cat_existente = False
        for categoria in categorias:
            if nome == categoria.esp_nome:
                flash('Categoria já existe')
                cat_existente = True

                return redirect(url_for('tecnico.cadastrar_categoria'))
                
        if not cat_existente: 
            nova_categoria = EspecialidadeLab(esp_nome = form['nome_categoria'])
    
    else:
        return "erro"
    db.session.add(nova_categoria)
    db.session.commit()

@tec_bp.route('/categorias', methods=['POST','GET'])
def cadastrar_categoria():
    if request.method == 'GET':
        return render_template('/pages/categoria.html')
    else:
        criar_categoria(request.form)
        flash('Categoria criada com sucesso!')
        return redirect(url_for('tecnico.cadastrar_categoria'))


