from ... import prof_bp
from ..services.user import find_user
from flask import render_template, redirect, url_for
from .....models import Material, Reagente, CategoriaReagente, CategoriaMaterial, ReservaItens, ReservaMaterial, ReservaReagente

@prof_bp.route('/')
def home():
    materiais_cadastrados = Material.query.count()
    reagentes_cadastrados = Reagente.query.count()
    itens_cadastrados = materiais_cadastrados + reagentes_cadastrados

    #Pegar reservas filtradas por id do usuário current_user
    #Separar as reservas entre soliciadas, pendentes e confirmadas
    #Pegar quantidade de aulas cadastradas ( Fazer as aulas primeiro )
    

    usuario = find_user()
    return render_template('home.html', nome = usuario.usu_nome, quantidade_material = itens_cadastrados)
