from flask import redirect, render_template, request, flash, url_for
from flask_login import current_user
from .....models import Material, Reagente, CategoriaReagente, CategoriaMaterial, ReservaItens, Lab, ReservaLab, ReservaMaterial, ReservaReagente
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

def get_categorias_reagentes():
    categorias = db.session.scalars(db.select(CategoriaReagente)).all()
    return categorias

def get_categorias_materiais():
    categorias = db.session.scalars(db.select(CategoriaMaterial)).all()
    return categorias


# materialservice.py
def cadastrar_reagente(form):
    try:
        print(">>> Recebendo form:", dict(form))

        # Nome
        nome_reagente = form.get('reagente')
        print(">>> Nome:", nome_reagente)

        # Categoria (select ou nova)
        tipo_reagente = form.get('tipo')
        rgt_cat_id = None

        if tipo_reagente:  # veio do select → já é ID
            rgt_cat_id = db.session.scalar(
                db.select(CategoriaReagente.cat_id).filter(CategoriaReagente.cat_id == int(tipo_reagente))
            )
            print(">>> Categoria ID selecionada:", rgt_cat_id)

        else:  # veio do input de nova categoria
            tipo_reagente = form.get('tipo_reagente_novo')
            print(">>> Nova categoria:", tipo_reagente)

            existente = db.session.scalar(
                db.select(CategoriaReagente).filter(CategoriaReagente.cat_nome == tipo_reagente)
            )
            if existente:
                return False, "Categoria já existe"
            else:
                nova_cat = CategoriaReagente(nome=tipo_reagente)
                db.session.add(nova_cat)
                db.session.commit()
                rgt_cat_id = nova_cat.cat_id
                print(">>> Nova categoria criada com ID:", rgt_cat_id)

        if not rgt_cat_id:
            return False, "Categoria inexistente"

        # Demais campos
        rgt_unidade = form.get('unidade')
        quantidade_reagente = form.get('quantidade')
        validade_reagente = form.get('validade')
        laboratorio = form.get('local')
        rgt_fornecedor = form.get('fornecedor')

        print(">>> Quantidade:", quantidade_reagente)
        print(">>> Unidade:", rgt_unidade)
        print(">>> Validade:", validade_reagente)
        print(">>> Local (ID):", laboratorio)
        print(">>> Fornecedor:", rgt_fornecedor)

        # Laboratório (sempre ID do select)
        rgt_lab_id = db.session.scalar(
            db.select(Lab.lab_id).filter(Lab.lab_id == int(laboratorio))
        )
        if not rgt_lab_id:
            return False, "Laboratório inexistente"

        # Cria reagente
        novo_reagente = Reagente(
            nome_reagente, quantidade_reagente, rgt_unidade,
            rgt_fornecedor, validade_reagente, rgt_lab_id, rgt_cat_id
        )
        db.session.add(novo_reagente)
        db.session.commit()

        print(">>> Reagente cadastrado com sucesso!")
        return True, "Reagente cadastrado com sucesso"

    except Exception as e:
        print(">>> ERRO AO CADASTRAR:", str(e))
        return False, f"Erro ao cadastrar reagente: {str(e)}"


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


def criar_reserva(reserva_lab_id, form):
    materiais = form.getlist['materiais']
    # reagentes = form.getlist['reagentes']

    # rgt_quantidade = form.getlist['rgt_quantidade']
    mat_quantidade = form.getlist['mat_quantidade']
    # rgt_unidade = form.getlist['rgt_unidade']

    nova_reserva = ReservaItens(reserva_lab_id) #Primeiro cria a reserva itens
    db.session.add(nova_reserva) #Coloca ela no banco
    db.session.flush() #E da flush pra conseguir recuperar o id dela e ainda dar 1 commit só

    #Aqui vai precisar de um for para criar as reservas dos materiais e reagentes.
    
    for material, quantidade in zip(materiais,mat_quantidade): #pegando o reagente direto, sem select, lembrar de não pegar por id no form
        res_material = ReservaMaterial(material_id = material.mat_id, reserva_itens_id = nova_reserva.rei_id, quantidade = quantidade) #Cria reserva
        material.mat_quantidade = material.mat_quantidade - quantidade #Subtrair quantidade no banco
        db.session.add(res_material)

    for reagente, quantidade in zip(reagentes, rgt_quantidade): #pegando o reagente direto, sem select, lembrar de não pegar por id no form
        res_reagente = ReservaReagente(reagente_id = 1, reserva_itens_id = nova_reserva.rei_id, quantidade = rgt_quantidade, unidade = reagente.rgt_unidade) #Cria reserva
        reagente.rgt_quantidade = reagente.rgt_quantidade - quantidade #Subtrair quantidade no banco
        db.session.add(res_reagente)

    db.session.commit()
    #return redirect(url_for(''))

    