from flask_login import current_user
from sqlalchemy import func
from .....database import db
from .....models import User, Lab, ReservaLab

#Buscar usuário
def find_user():
    usuario = db.session.scalar(db.select(User).where(User.usu_matricula == current_user.usu_matricula))

    return usuario

def get_labs():
    laboratorios = db.session.scalars(db.select(Lab)).all()

    return laboratorios

def reservas_usuario():
    pendentes = 0
    confirmadas = 0
    total_reservas = db.session.scalar(db.select(func.count()).select_from(ReservaLab).where(ReservaLab.rel_usu_matricula == current_user.usu_matricula))
    reservas = db.session.scalars(db.select(ReservaLab).where(ReservaLab.rel_usu_matricula == current_user.usu_matricula))
    for reserva in reservas:
        if reserva.rel_status == "Pendente":
            pendentes += 1
        elif reserva.rel_status == "Confirmada":
            confirmadas += 1

    return total_reservas, pendentes, confirmadas