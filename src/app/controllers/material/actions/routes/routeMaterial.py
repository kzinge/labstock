from flask import render_template, request, redirect, url_for, flash
from ... import materiais_bp
from ..services import materialservice
#IMPORTAR ROLE_REQUIRED

##### REAGENTES #####

@materiais_bp.route('/', methods=['POST','GET']) # ROTA APENAS PARA TECNICO E PROFESSORES
# @role_required('Docente') #IMPORTAR ROLE_REQUIRED
def estoque():
    reagentes = materialservice.get_reagentes() ; materiais = materialservice.get_materiais()
    return render_template('materiais/estoque.html', reagentes = reagentes, materiais = materiais)


 
@materiais_bp.route('/visualizar_estoque', methods=['POST','GET']) #Amigo essa rota que eu criei seria referente a fucionalidade vizualizar da pagina de estoque
def visualizar_estoque(): 
    reagentes = materialservice.get_reagentes()
    materiais = materialservice.get_materiais()
    return render_template('materiais/view_estoque.html', reagentes=reagentes, materiais=materiais)



@materiais_bp.route('/cadastro_reagente', methods=['POST', 'GET']) # ROTA APENAS PARA TECNICO ######
def cadastro():
    laboratorios = materialservice.get_labs() ; categorias = materialservice.get_categorias_reagentes()
    return render_template('materiais/cadastrar_reagente.html' , categorias=categorias, laboratorios=laboratorios)



@materiais_bp.route('/cadastro_reagente', methods=['POST'])
# @role_required('Técnico') #IMPORTAR ROLE_REQUIRED
def cadastro_reagente():
    materialservice.cadastrar_material()



@materiais_bp.route('/edit_reagente/<int:id>', methods=['POST', 'GET']) # ROTA APENAS PARA TECNICO
def edit_reagente(id):
    materialservice.edit_reagente(id, request.method)



@materiais_bp.route('/remove_rgt/<int:id>', methods=['POST', 'GET']) # ROTA APENAS PARA TECNICO
def remove_reagente(id):
    materialservice.remover_reagente(id)


##### MATERIAIS #####

@materiais_bp.route('/cadastrar_material', methods=['POST','GET'])
def cadastro_material():
    return render_template('materiais/cadastrar_material.html')
    #materialservice.cadastrar_material(request.form)

@materiais_bp.route('/delete_material/<int:id>', methods=['POST'])
def remove_material(id):
    materialservice.remover_material(id)

@materiais_bp.route('/reservar/<int:lab_id>', methods=['POST','GET'])
def cadastrar_reserva(lab_id):
    if request.method == 'GET':
        return render_template('materiais/reservar_materiais.html')
    else:
        materialservice.criar_reserva(lab_id, request.form)