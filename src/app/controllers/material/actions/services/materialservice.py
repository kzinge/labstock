from flask import redirect, render_template, request, flash, url_for
from flask_login import current_user
from .....models import Material, Reagente, CategoriaReagente, CategoriaMaterial, ReservaMaterial, Lab
from .....database import db
from .....decorators.auth import role_required
from datetime import datetime, date

################################################################
################## FUNÇÕES DE SELECT DO BANCO ##################
################################################################


def get_reagentes():
    reagentes = db.session.scalars(db.select(Reagente)).all()
    return reagentes

def get_materiais():
    materiais = db.session.scalars(db.select(Material)).all()
    return materiais

def get_labs():
    labs = db.session.scalars(db.select(Lab)).all()
    return labs

def get_categorias():
    categorias = db.session.scalars(db.select(CategoriaReagente)).all()
    return categorias


def cadastrar_material(form):
    nome_reagente = request.form['nome_reagente']

    try:  # Tenta pegar do select
        tipo_reagente = request.form['tipo_reagente']

    except:  # Se der erro é por que ta com o input de criar uma categoria nova
        tipo_reagente = request.form['tipo_reagente_novo']
        categorias = db.session.scalars(db.select(CategoriaReagente)).all()

        if not categorias:  # caso não exista categoria ainda, ele cria a que a pessoa colocou
            nova_cat = CategoriaReagente(nome=tipo_reagente)
            db.session.add(nova_cat)
            db.session.commit()

        for categoria in categorias:
            if tipo_reagente == categoria.cat_nome:
                flash('CategoriaReagente já existe')
                return redirect(url_for('material.cadastro'))
            else:
                nova_cat = CategoriaReagente(nome=tipo_reagente)
                db.session.add(nova_cat)
                db.session.commit()
                break

    rgt_unidade = request.form['unidade']
    quantidade_reagente = request.form['quantidade_reagente']
    validade_reagente = request.form['validade_reagente']
    laboratorio = request.form['lab_local']
    rgt_fornecedor = request.form['fornecedor_reagente']

    rgt_cat_id = db.session.scalar(db.select(CategoriaReagente.cat_id).filter(
        CategoriaReagente.cat_nome == tipo_reagente))
    if not rgt_cat_id:  # ESSE IF NÃO PRECISA MAIS, TA SENDO PEGA POR SELECT
        flash('CategoriaReagente inexistente')
        return render_template('materiais/cadastrar_material.html')
    rgt_lab_id = db.session.scalar(
        db.select(Lab.lab_id).filter(Lab.lab_sala == laboratorio))

    if not rgt_lab_id:  # ESSE IF NÃO PRECISA MAIS, TA SENDO PEGA POR SELECT
        flash('Laboratório inexistente')
        return render_template('materiais/cadastrar_material.html')

    novo_reagente = Reagente(nome_reagente, quantidade_reagente, rgt_unidade,
                             rgt_fornecedor, validade_reagente, rgt_lab_id, rgt_cat_id)
    db.session.add(novo_reagente)
    db.session.commit()
    return redirect(url_for('material.estoque'))


def editar_reagente(id, method):
    
    reagente = db.session.scalar(db.select(Reagente).filter(Reagente.rgt_id == int(id)))
    categoria = db.session.scalar(db.select(CategoriaReagente.cat_nome).filter(CategoriaReagente.cat_id == Reagente.rgt_cat_id))
    laboratorio = db.session.scalar(db.select(Lab).filter(Lab.lab_id == reagente.rgt_lab_id))

    if method == 'POST':
        nome_reagente = request.form['nome_reagente']
        tipo_reagente = request.form['tipo_reagente']
        rgt_unidade = request.form['unidade']
        quantidade_reagente = request.form['quantidade_reagente']
        validade_reagente = request.form['validade_reagente']
        laboratorio_novo = request.form['lab_nome']
        rgt_fornecedor = request.form['fornecedor']

        if nome_reagente != reagente.rgt_nome:
            reagente.rgt_nome = nome_reagente

        if tipo_reagente != categoria: 
            rgt_cat_id = db.session.scalar(db.select(CategoriaReagente.cat_id).filter(CategoriaReagente.cat_nome == tipo_reagente))
            if not rgt_cat_id:
                flash('CategoriaReagente inválida')
                return render_template('materiais/edit_reagente.html', reagente = reagente, categoria = categoria, laboratorio = laboratorio)
            reagente.rgt_cat_id = rgt_cat_id

        if rgt_unidade != reagente.rgt_unidade:
            reagente.rgt_unidade = rgt_unidade

        if quantidade_reagente != reagente.rgt_quantidade:
            reagente.rgt_quantidade = quantidade_reagente

        if validade_reagente != reagente.rgt_validade:
            reagente.rgt_validade = validade_reagente 

        if laboratorio_novo != laboratorio:
            rgt_lab_id = db.session.scalar(db.select(Lab.lab_id).filter(Lab.lab_sala == laboratorio_novo))
            if not rgt_lab_id:
                flash('Laboratório inválido')
                return render_template('materiais/edit_reagente.html', reagente = reagente, categoria = categoria, laboratorio = laboratorio)
            reagente.rgt_lab_id = rgt_lab_id

        if rgt_fornecedor != reagente.rgt_fornecedor:
            reagente.rgt_fornecedor = rgt_fornecedor
        
        db.session.commit()
        return redirect(url_for('material.estoque'))
        
    return render_template('materiais/edit_reagente.html', material = reagente, categoria = categoria, laboratorio = laboratorio)



def remover_reagente(id):
    reagente = db.session.scalar(db.select(Reagente).filter(Reagente.rgt_id == int(id)))
    db.session.delete(reagente)
    db.session.commit()
    return redirect(url_for('material.estoque'))





##### MATERIAIS #####

def cadastrar_material(form):
    nome = form['nome_material']
    descricao = form['descricao']
    quantidade = form['quantidade_material']
    fornecedor = form['fornecedor_material']
    validade = form['validade_material']
    lab = form['lab_material']
    cat = form['categoria_material']
    
    cat_id = db.session.scalar(db.select(CategoriaReagente.cat_id).filter(CategoriaReagente.cat_nome == cat))
    lab_id = db.session.scalar(db.select(Lab.lab_id).filter(Lab.lab_sala == lab))

    novo_material = Material(nome, descricao, quantidade, fornecedor, validade, lab_id, cat_id)

    db.session.add(novo_material)
    db.session.commit()

    return redirect(url_for('material.estoque'))

def remover_material(id):
    material = db.session.scalar(db.select(Material).filter(Material.mat_id == int(id)))
    db.session.delete(material)
    db.session.commit()
    return redirect(url_for('material.estoque'))
