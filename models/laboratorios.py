from sqlalchemy import Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import db
from datetime import datetime

class Lab(db.Model):
    __tablename__ = 'tb_laboratorios'

    lab_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lab_nome: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    lab_local: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    lab_capacidade: Mapped[int] = mapped_column(Integer, nullable=False)
    lab_especialidade: Mapped[Enum] = mapped_column(Enum('Química', 'Biologia'), nullable=False)

    materiais = relationship('Material', back_populates='laboratorio', lazy=True)
    reservas = relationship('ReservaLab', back_populates='laboratorio', lazy=True)

    def __repr__(self):
        return f'Lab {self.lab_nome} - {self.lab_local}'

    def __init__(self, nome, local, capacidade, especialidade) -> None:
        self.lab_nome = nome
        self.lab_local = local
        self.lab_capacidade = capacidade
        self.lab_especialidade = especialidade

class ReservaLab(db.Model):
    __tablename__ = 'tb_reservas_laboratorios'

    rel_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rel_data: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    rel_motivo: Mapped[str] = mapped_column(Text, nullable=False)
    rel_tipo: Mapped[str] = mapped_column(Enum('Anual', 'Semestral', 'Extraordinária'), nullable=False)
    rel_lab_id: Mapped[int] = mapped_column(ForeignKey('tb_laboratorios.lab_id'), nullable=False)
    rel_usu_matricula: Mapped[str] = mapped_column(String(20), ForeignKey('tb_usuarios.usu_matricula'), nullable=False)
    
    laboratorio = relationship('Lab', back_populates='reservas', lazy=True)
    reservas_materiais = relationship('ReservaMaterial', back_populates='reserva', lazy=True)

    def __repr__(self):
        return f'Reserva {self.rel_id} - Laboratório: {self.rel_lab_id} - Data: {self.rel_data}'

    def __init__(self, data, motivo, tipo, lab_id, usu_matricula) -> None:
        self.rel_data = data
        self.rel_motivo = motivo
        self.rel_tipo = tipo
        self.rel_lab_id = lab_id
        self.rel_usu_matricula = usu_matricula