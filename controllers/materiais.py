#Rotas para materiais
from flask import Blueprint, render_template, redirect, url_for, request
from ..database import db
from ..models.materiais import Material, Categoria
materiais_bp = Blueprint(name ='material', 
                    import_name= __name__, 
                    url_prefix='/material', 
                    template_folder='templates')

#CREATE MATERIAIS
@materiais_bp.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    #Variaveis temporarias por que não tem input pra elas, alterar depois !!!!!!!!!!!!!!
    #isso COM CERTEZA ta dando erro, ja to avisando
    #pra criar material precisa ja existir categorias cadastradas, laboratorios cadastrados e de campos para informar o fornecedor e unidade.
    #isso n tem como ser testado por agora (momento que estou fazendo isso)
    mat_fornecedor = 'null'
    mat_lab_id = 1 #PEGAR O LABORATORIO
    if request.method == 'POST':
        nome_material = request.form['nome_material']
        tipo_material = request.form['tipo_material'] #Vou achar que esse tipo é a Categoria
        mat_unidade = request.form['unidade']
        quantidade_material = request.form['quantidade_material']
        validade_material = request.form['validade_material']
        mat_cat_id = db.session.scalar(db.select(Categoria.cat_id).filter(Categoria.cat_nome == tipo_material))
        novo_material = Material(nome_material, quantidade_material, mat_unidade, 
                                 mat_fornecedor, validade_material, mat_lab_id, mat_cat_id)
        db.session.add(novo_material)
        db.session.commit()
        return redirect(url_for('material.estoque'))
    return render_template('materiais/cadastrar_material.html')

@materiais_bp.route('/edit/<int:id>', methods=['POST', 'GET']) # AINDA PRECISA LEMBRAR DE MUDAR O NEGÓCIO PRA PEGAR O LABORATORIO
def edit(id):
    material = db.session.scalar(db.select(Material).filter(Material.mat_id == int(id)))
    categoria = db.session.scalar(db.select(Categoria.cat_nome).filter(Categoria.cat_id == material.mat_cat_id))

    print(f'material: {material.mat_nome} {material.mat_id} | categoria: {categoria}') # PRINT PRA DEBUG, LEMBRAR DE REMOVER AAAAAAA
    if request.method == 'POST':
        nome_material = request.form['nome_material']
        tipo_material = request.form['tipo_material']
        mat_unidade = request.form['unidade']
        quantidade_material = request.form['quantidade_material']
        validade_material = request.form['validade_material']

        if nome_material != material.mat_nome:
            material.mat_nome = nome_material
        if tipo_material != categoria: 
            mat_cat_id = db.session.scalar(db.select(Categoria.cat_id).filter(Categoria.cat_nome == tipo_material))
            material.mat_cat_id = mat_cat_id
        if mat_unidade != material.mat_unidade:
            material.mat_unidade = mat_unidade
        if quantidade_material != material.mat_quantidade:
            material.mat_quantidade = quantidade_material
        if validade_material != material.mat_validade:
            material.mat_validade = validade_material 
        
        return redirect(url_for('estoque'))

    return render_template('materiais/edit_material.html', material = material, categoria = categoria)

@materiais_bp.route('/estoque', methods=['POST','GET'])
def estoque():
    materiais = db.session.scalars(db.select(Material)).all()
    return render_template('materiais/estoque.html', materiais = materiais)

@materiais_bp.route('/nova_categoria', methods=['POST'])
def nova_categoria():
    nome = request.form['nome']
    nova_cat = Categoria(nome=nome)
    db.session.add(nova_cat)
    db.session.commit()
    
    return redirect(url_for('material.cadastrar_material'))

