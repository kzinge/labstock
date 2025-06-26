from ... import prof_bp
from ..services.user import find_user,reservas_usuario
from flask import render_template, redirect, url_for
from .....models import Material, Reagente, CategoriaReagente, CategoriaMaterial, ReservaItens, ReservaMaterial, ReservaReagente

@prof_bp.route('/')
def home():
    materiais_cadastrados = Material.query.count()
    reagentes_cadastrados = Reagente.query.count()
    itens_cadastrados = materiais_cadastrados + reagentes_cadastrados

    #Pegar quantidade de aulas cadastradas ( Fazer as aulas primeiro )
    
    reservas = reservas_usuario()
    total_reservas = reservas[0]
    pendentes = reservas[1]
    confirmadas = reservas[2]

    usuario = find_user()
    return render_template('home.html', nome = usuario.usu_nome, quantidade_material = itens_cadastrados,
                            total_reservas = total_reservas, pendentes = pendentes, confirmadas = confirmadas)
