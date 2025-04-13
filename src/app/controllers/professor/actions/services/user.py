from flask_login import current_user
from .....database import db
from .....models import User, Lab, ReservaLab

#Buscar usuário
def find_user():
    usuario = db.session.scalar(db.select(User).where(User.usu_matricula == current_user.usu_matricula))

    return usuario

def get_labs():
    laboratorios = db.session.scalars(db.select(Lab)).all()

    return laboratorios