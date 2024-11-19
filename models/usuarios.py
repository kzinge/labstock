from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from ..database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):

    __tablename__ = 'tb_usuarios'


    usu_id: Mapped[int] = mapped_column(Integer, primary_key = True)
    usu_nome: Mapped[str] = mapped_column(String(100), nullable = False)
    usu_email: Mapped[str] = mapped_column(String(150), nullable = False, unique= True)
    # usu_matricula: Mapped[str] = mapped_column(String(20), nullable= False, unique = True)
    # usu_tipo: Mapped[str] = mapped_column(String(150), nullable= False)

    def __repr__(self):
        return f'User {self.usu_nome} - {self.usu_email}'
    
    def __init__(self, nome, email) -> None:
        self.usu_nome = nome
        self.usu_email = email
        # self.usu_matricula = matricula
        # self.usu_tipo = tipo