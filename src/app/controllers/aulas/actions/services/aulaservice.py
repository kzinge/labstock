from flask import render_template,request, redirect, url_for, flash
from flask_login import current_user
from .....models import Aula, Lab
from .....database import db
from datetime import datetime, date
from .....decorators.auth import role_required
from ....laboratorio.actions.services import labservice

def cadastrar_aula(form):
    aul_titulo = form['titulo']
    aul_desc = form['desc']
    aul_horarioInicio = form['horarioInicio']
    aul_horarioTermino = form['horarioTermino']
    aul_data = form['data']

    aul_lab_id = form['lab']

    aul_usu_id = current_user.usu_matricula

    aula = Aula(
        aul_titulo=aul_titulo,
        aul_desc=aul_desc,
        aul_horarioInicio=aul_horarioInicio,
        aul_horarioTermino=aul_horarioTermino,
        aul_data=aul_data,
        aul_lab_id=aul_lab_id,
        aul_usu_id=aul_usu_id
    )

    try:
        db.session.add(aula)
        db.session.commit()
        return True, "Aula cadastrada com sucesso!"
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao cadastrar aula: {e}")
        return False, f"Erro ao cadastrar aula: {e}"
    

def get_aulas():
    try:
        aulas = db.session.scalars(db.select(Aula)).all()
        return aulas
    except Exception as e:
        print(f"Erro ao obter aulas: {e}")
        return []