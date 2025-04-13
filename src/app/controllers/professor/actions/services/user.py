from flask_login import current_user
from .....database import db
from .....models import User

#Buscar usuário
def find_user():
    usuario = db.session.scalar(db.select(User).where(User.usu_matricula == current_user.usu_matricula))

    return usuario