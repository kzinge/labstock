from sqlalchemy import Integer, String, Date, Time, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import db
from datetime import datetime, date, time

class EspecialidadeLab(db.Model):
    __tablename__ = 'tb_especialidades_labs'

    esp_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    esp_nome: Mapped[str] = mapped_column(String(50), nullable=False)

    laboratorio = relationship('Lab', back_populates='especialidades', lazy=True)

class Lab(db.Model):
    __tablename__ = 'tb_laboratorios'

    lab_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lab_nome: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    lab_bloco: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    lab_sala: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    lab_capacidade: Mapped[int] = mapped_column(Integer, nullable=False)
    lab_especialidade: Mapped[int] = mapped_column(Integer, ForeignKey('tb_especialidades_labs.esp_id'), nullable=False)

    materiais = relationship('Material', back_populates='laboratorio', lazy=True)
    reagentes = relationship('Reagente', back_populates='laboratorio', lazy=True)
    reservas = relationship('ReservaLab', back_populates='laboratorio', lazy=True)  
    especialidades = relationship('EspecialidadeLab', back_populates='laboratorio', lazy=True)

    def __repr__(self):
        return f'Lab {self.lab_nome} - {self.lab_local}'

    def __init__(self, nome, bloco, sala, capacidade, especialidade) -> None:
        self.lab_nome = nome
        self.lab_bloco = bloco
        self.lab_sala = sala
        self.lab_capacidade = capacidade
        self.lab_especialidade = especialidade

class ReservaLab(db.Model):
    __tablename__ = 'tb_reservas_laboratorios'

    rel_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rel_dataInicial: Mapped[date] = mapped_column(Date, nullable=False)
    rel_dataFinal: Mapped[date] = mapped_column(Date, nullable=False)
    rel_horarioInicial: Mapped[time] = mapped_column(Time, nullable=False)
    rel_horarioFinal: Mapped[time] = mapped_column(Time, nullable=False)
    rel_motivo: Mapped[str] = mapped_column(Text, nullable=False)
    rel_tipo: Mapped[str] = mapped_column(Enum('Anual', 'Semestral', 'Extraordinária'), nullable=False)
    rel_status: Mapped[str] = mapped_column(Enum('Pendente', 'Confirmada', 'Rejeitada'), nullable=False, default='Pendente')
    rel_lab_id: Mapped[int] = mapped_column(ForeignKey('tb_laboratorios.lab_id'), nullable=False)
    rel_usu_matricula: Mapped[str] = mapped_column(String(20), ForeignKey('tb_usuarios.usu_matricula'), nullable=False)
    
    laboratorio = relationship('Lab', back_populates='reservas', lazy=True)
    usuario = relationship('User', back_populates='reservas', lazy=True)
    reservas_itens = relationship('ReservaItens', back_populates='reserva_lab', lazy=True)

    def __repr__(self):
        return f'Reserva {self.rel_id} - Laboratório: {self.laboratorio} - Data Inicial: {self.rel_dataInicial} - até {self.rel_dataFinal} de {self.rel_horarioInicial} às {self.rel_horarioFinal}'

    def __init__(self, data_inicial, data_final, horario_inicial, horario_final, motivo, tipo, lab_id, usu_matricula) -> None:
        self.rel_dataInicial = data_inicial
        self.rel_dataFinal = data_final
        self.rel_horarioInicial = horario_inicial
        self.rel_horarioFinal = horario_final
        self.rel_motivo = motivo
        self.rel_tipo = tipo
        self.rel_lab_id = lab_id
        self.rel_usu_matricula = usu_matricula