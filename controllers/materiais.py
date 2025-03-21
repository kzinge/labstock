#Rotas para materiais
from flask import Blueprint, render_template, redirect, url_for, request, flash
from database import db
from models.materiais import Material, Reagente, Categoria
from models.laboratorios import Lab
from decorators.auth import role_required
materiais_bp = Blueprint(name ='material',
                    import_name= __name__, 
                    url_prefix='/material', 
                    template_folder='templates')


@materiais_bp.route('/', methods=['POST','GET']) # ROTA APENAS PARA TECNICO E PROFESSORES
# @role_required('Docente')
def estoque():
    materiais = db.session.scalars(db.select(Reagente)).all()
    return render_template('materiais/estoque.html', materiais = materiais)

#REAGENTES

@materiais_bp.route('/cadastro', methods=['POST', 'GET']) # ROTA APENAS PARA TECNICO
def cadastro():
    categorias = db.session.scalars(db.select(Categoria)).all()
    return render_template('materiais/cadastrar_material.html' , categorias=categorias)

@materiais_bp.route('/cadastro_reagente', methods=['POST','GET'])
def cadastro_reagente():
    if request.method == 'POST':
        nome_reagente = request.form['nome_reagente']

        try: #Tenta pegar do select
            tipo_reagente = request.form['tipo_reagente']

        except: #Se der erro é por que ta com o input de criar uma categoria nova

            tipo_reagente = request.form['tipo_reagente_novo']
            categorias = db.session.scalars(db.select(Categoria)).all()
            
            for categoria in categorias:
                if tipo_reagente == categoria.cat_nome:
                    flash('Categoria já existe')
                    return redirect(url_for('material.cadastro'))
                else:
                    nova_cat = Categoria(nome = tipo_reagente)
                    db.session.add(nova_cat)
                    db.session.commit()
                    break

        rgt_unidade = request.form['unidade']
        quantidade_reagente = request.form['quantidade_reagente']
        validade_reagente = request.form['validade_reagente']
        laboratorio = request.form['lab_nome']
        rgt_fornecedor = request.form['fornecedor']

        rgt_cat_id = db.session.scalar(db.select(Categoria.cat_id).filter(Categoria.cat_nome == tipo_reagente))
        if not rgt_cat_id:
            flash('Categoria inexistente')
            return render_template('materiais/cadastrar_material.html',nome=nome_reagente, unidade=rgt_unidade, 
                quantidade=quantidade_reagente, validade=validade_reagente, laboratorio=laboratorio, fornecedor = rgt_fornecedor)
        rgt_lab_id = db.session.scalar(db.select(Lab.lab_id).filter(Lab.lab_nome == laboratorio))
        if not rgt_lab_id:
            flash('Laboratório inexistente')
            return render_template('materiais/cadastrar_material.html',nome=nome_reagente, unidade=rgt_unidade, 
                quantidade=quantidade_reagente, validade=validade_reagente, categoria = tipo_reagente, fornecedor = rgt_fornecedor)
        


        novo_reagente = Reagente(nome_reagente, quantidade_reagente, rgt_unidade, 
                                     rgt_fornecedor, validade_reagente, rgt_lab_id, rgt_cat_id)
        db.session.add(novo_reagente)
        db.session.commit()
        return redirect(url_for('material.estoque'))


@materiais_bp.route('/edit/<int:id>', methods=['POST', 'GET']) # ROTA APENAS PARA TECNICO
def edit(id):
    reagente = db.session.scalar(db.select(Reagente).filter(Reagente.rgt_id == int(id)))
    categoria = db.session.scalar(db.select(Categoria.cat_nome).filter(Categoria.cat_id == Reagente.rgt_cat_id))
    laboratorio = db.session.scalar(db.select(Lab.lab_nome).filter(Lab.lab_id == reagente.rgt_lab_id))

    print(f'reagente: {reagente.rgt_nome} {reagente.rgt_id} | categoria: {categoria}')
    if request.method == 'POST':
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
            rgt_cat_id = db.session.scalar(db.select(Categoria.cat_id).filter(Categoria.cat_nome == tipo_reagente))
            if not rgt_cat_id:
                flash('Categoria inválida')
                return render_template('materiais/edit_reagente.html', reagente = reagente, categoria = categoria, laboratorio = laboratorio)
            reagente.rgt_cat_id = rgt_cat_id

        if rgt_unidade != reagente.rgt_unidade:
            reagente.rgt_unidade = rgt_unidade

        if quantidade_reagente != reagente.rgt_quantidade:
            reagente.rgt_quantidade = quantidade_reagente

        if validade_reagente != reagente.rgt_validade:
            reagente.rgt_validade = validade_reagente 

        if laboratorio_novo != laboratorio:
            rgt_lab_id = db.session.scalar(db.select(Lab.lab_id).filter(Lab.lab_nome == laboratorio_novo))
            if not rgt_lab_id:
                flash('Laboratório inválido')
                return render_template('materiais/edit_reagente.html', reagente = reagente, categoria = categoria, laboratorio = laboratorio)
            reagente.rgt_lab_id = rgt_lab_id

        if rgt_fornecedor != reagente.rgt_fornecedor:
            reagente.rgt_fornecedor = rgt_fornecedor
        
        db.session.commit()
        return redirect(url_for('material.estoque'))
        
    return render_template('materiais/edit_reagente.html', material = reagente, categoria = categoria, laboratorio = laboratorio)



@materiais_bp.route('/remove/<int:id>', methods=['POST', 'GET']) # ROTA APENAS PARA TECNICO
def remove(id):
    reagente = db.session.scalar(db.select(reagente).filter(reagente.rgt_id == int(id)))
    db.session.delete(reagente)
    db.session.commit()
    return redirect(url_for('material.estoque'))



@materiais_bp.route('/reservar', methods=['POST','GET'])
def reservar():
    pass



# @materiais_bp.route('/nova_categoria', methods=['POST']) # ROTA APENAS PARA TECNICO
# def nova_categoria():
#     nome = request.form['nome']
#     nova_cat = Categoria(nome=nome)
#     db.session.add(nova_cat)
#     db.session.commit()
    
    return redirect(url_for('reagente.cadastro'))





#materiais

@materiais_bp.route('/novo_material')
def cadastro_material():
    return render_template('materiais/edit_reagente.html')