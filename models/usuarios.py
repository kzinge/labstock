from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):

    __tablename__ = 'tb_usuarios'

    usu_matricula: Mapped[str] = mapped_column(String(20), nullable= False, primary_key= True)
    usu_nome: Mapped[str] = mapped_column(String(100), nullable = False)
    usu_email: Mapped[str] = mapped_column(String(150), nullable = False, unique= True)
    usu_tipo: Mapped[str] = mapped_column(String(150), nullable= False)
    usu_foto: Mapped[str] = mapped_column(String(200))

    reservas = relationship('ReservaLab', back_populates='usuario', lazy=True)

    def __repr__(self):
        return f'User {self.usu_nome} - {self.usu_email}'

    def get_id(self):
        return self.usu_matricula  # Retorna o ID do usuário
    
    def __init__(self, nome,email, matricula,tipo,foto) -> None:
        self.usu_nome = nome
        self.usu_email = email
        self.usu_matricula = matricula
        self.usu_tipo = tipo
        self.usu_foto = foto
