#Rotas para materiais
from flask import Blueprint, render_template, redirect, url_for, request
from ..database import db
from ..models.materiais import Material, Categoria
materiais_bp = Blueprint(name ='material', 
                    import_name= __name__, 
                    url_prefix='/material', 
                    template_folder='templates')

#CREATE MATERIAIS
@materiais_bp.route('/cadastrar_material', methods=['POST', 'GET'])
def cadastrar_material():
    #Variaveis temporarias por que não tem input pra elas, alterar depois !!!!!!!!!!!!!!
    #isso COM CERTEZA ta dando erro, ja to avisando
    #pra criar material precisa ja existir categorias cadastradas, laboratorios cadastrados e de campos para informar o fornecedor e unidade.
    #isso n tem como ser testado por agora (momento que estou fazendo isso)
    mat_fornecedor = 'null'
    mat_unidade = 'null'
    mat_lab_id = 'null'
    if request.method == 'POST':
        nome_material = request.form['nome_material']
        tipo_material = request.form['tipo_material'] #Vou achar que esse tipo é a Categoria
        quantidade_material = request.form['quantidade_material']
        validade_material = request.form['validade_material']
        mat_cat_id = db.session.scalar(db.select(Categoria.cat_id).filter(Categoria.cat_nome == tipo_material)) #se der erro aq, trocar filter por where
        novo_material = Material(mat_nome = nome_material, mat_quantidade = quantidade_material, mat_unidade = mat_unidade, 
                                 mat_fornecedor = mat_fornecedor, mat_validade = validade_material, mat_lab_id = mat_lab_id, mat_cai_id = mat_cat_id)
        db.session.add(novo_material)
        db.session.commit()
        return redirect(url_for('material.estoque'))
    return render_template('materiais/cadastrar_material.html')

@materiais_bp.route('/estoque', methods=['POST','GET'])
def estoque():
    materiais = db.session.scalars(db.select(Material)).all()
    return render_template('estoque.html', materiais = materiais)

@materiais_bp.route('/nova_cat', methods=['POST'])
def nova_categoria():
    nome = request.form['nome']
    nova_cat = Categoria(nome=nome)
    db.session.add(nova_cat)
    db.session.commit()
    
    return redirect(url_for('material.cadastrar_material'))