#Rotas para técnicos
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from ...database import db
from ...models import User
from ..material.actions.services import materialservice
from ..laboratorio.actions.services import labservice
from ...models import CategoriaMaterial, CategoriaReagente, EspecialidadeLab

tec_bp = Blueprint(
    name='tecnico',
    import_name=__name__,
    url_prefix='/tecnico',
    template_folder='templates/pages'
)

@tec_bp.route('/')
def index():
    num_labs = len(labservice.carregar_labs())
    num_mats = len(materialservice.get_materiais())
    num_reservas = len(labservice.carregar_reservas())
    num_novas_reservas = len(labservice.carregar_reservas_pendentes())
    return render_template(
        'pages/inicioTecnico.html',
        num_labs=num_labs,
        num_mats=num_mats,
        num_reservas=num_reservas,
        num_novas_reservas=num_novas_reservas
    )

# Função auxiliar para criar categorias
def criar_categoria(form):
    tipo = form.get("tipo")
    nome = form.get("nome_categoria")
    cat_existente = False
    nova_categoria = None

    if tipo == "material":
        categorias = materialservice.get_categorias_materiais()
        if categorias:
            for categoria in categorias:
                if nome == categoria.cat_nome:
                    flash('Categoria já existe')
                    cat_existente = True
                    return None
        if not cat_existente:
            nova_categoria = CategoriaMaterial(nome)

    elif tipo == "reagente":
        categorias = materialservice.get_categorias_reagentes()
        if categorias:
            for categoria in categorias:
                if nome == categoria.cat_nome:
                    flash('Categoria já existe')
                    cat_existente = True
                    return None
        if not cat_existente:
            nova_categoria = CategoriaReagente(nome)

    elif tipo == "lab":
        categorias = labservice.listar_especialidades()
        if categorias:
            for categoria in categorias:
                if nome == categoria.esp_nome:
                    flash('Categoria já existe')
                    cat_existente = True
                    return None
        if not cat_existente:
            nova_categoria = EspecialidadeLab(esp_nome=nome)

    else:
        flash("Erro: tipo de categoria inválido")
        return None

    if nova_categoria:
        db.session.add(nova_categoria)
        db.session.commit()
        return nova_categoria
    return None

# Rota para cadastrar categorias
@tec_bp.route('/categorias', methods=['POST', 'GET'])
def cadastrar_categoria():
    if request.method == 'GET':
        # renderiza a página com o formulário de categoria
        return render_template('/pages/categoria.html')

    else:
        nova_categoria = criar_categoria(request.form)
        if nova_categoria:
            flash('Categoria criada com sucesso!')
        return redirect(url_for('tecnico.cadastrar_categoria'))
