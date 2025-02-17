from sqlalchemy import Integer, String, DECIMAL, Numeric, Date, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import db
from datetime import date

class Categoria(db.Model):
    __tablename__ = 'tb_categorias'

    cat_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cat_nome: Mapped[str] = mapped_column(String(50), nullable=False)

    materiais = relationship('Material', back_populates='categoria', lazy=True)

    def __repr__(self):
        return self.cat_nome
    
    def __init__(self, nome) -> None:
        self.cat_nome = nome

class Material(db.Model):
    __tablename__ = 'tb_materiais'

    mat_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mat_nome: Mapped[str] = mapped_column(String(50), nullable=False)
    mat_quantidade: Mapped[DECIMAL] = mapped_column(Numeric(10, 2), nullable=False)
    mat_unidade: Mapped[Enum] = mapped_column(Enum('kg', 'g', 'mg', 'l', 'ml'), nullable=False)
    mat_fornecedor: Mapped[str] = mapped_column(String(90), nullable=False)
    mat_validade: Mapped[date] = mapped_column(Date, nullable=False)
    mat_lab_id: Mapped[int] = mapped_column(ForeignKey('tb_laboratorios.lab_id'), nullable=False)
    mat_cat_id: Mapped[int] = mapped_column(ForeignKey('tb_categorias.cat_id'), nullable=False)

    laboratorio = relationship('Lab', back_populates='materiais', lazy=True)
    categoria = relationship('Categoria', back_populates='materiais', lazy=True)
    reservas_materiais = relationship('ReservaMaterial', back_populates='material', lazy=True)

    def __repr__(self):
        return f'Material {self.mat_nome} - Quantidade: {self.mat_quantidade}'

    def __init__(self, nome, quantidade, unidade, fornecedor, validade, lab_id, cat_id) -> None:
        self.mat_nome = nome
        self.mat_quantidade = quantidade
        self.mat_unidade = unidade
        self.mat_fornecedor = fornecedor
        self.mat_validade = validade
        self.mat_lab_id = lab_id
        self.mat_cat_id = cat_id

class ReservaMaterial(db.Model):
    __tablename__ = 'tb_reservas_materiais'

    rem_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rem_mat_id: Mapped[int] = mapped_column(ForeignKey('tb_materiais.mat_id'), nullable=False)
    rem_rel_id: Mapped[int] = mapped_column(ForeignKey('tb_reservas_laboratorios.rel_id'), nullable=False)

    material = relationship('Material', back_populates='reservas_materiais', lazy=True)
    reserva = relationship('ReservaLab', back_populates='reservas_materiais', lazy=True)

    def __repr__(self):
        return f'Reserva Material {self.rem_id} - Material ID: {self.rem_mat_id} - Reserva ID: {self.rem_rel_id}'

    def __init__(self, mat_id, rel_id) -> None:
        self.rem_mat_id = mat_id
        self.rem_rel_id = rel_id