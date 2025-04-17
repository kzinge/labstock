from sqlalchemy import Integer, String, DECIMAL, Numeric, Date, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import db
from datetime import date
from typing import List

class CategoriaReagente(db.Model):
    __tablename__ = 'tb_categorias_reagentes'

    cat_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cat_nome: Mapped[str] = mapped_column(String(50), nullable=False)

    reagentes = relationship('Reagente', back_populates='categoria', lazy=True)

    def __repr__(self):
        return self.cat_nome
    
    def __init__(self, nome) -> None:
        self.cat_nome = nome


class CategoriaMaterial(db.Model):
    __tablename__ = 'tb_categorias_materiais'

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
    mat_descricao: Mapped[str] = mapped_column(String(200), nullable=False)
    mat_quantidade: Mapped[DECIMAL] = mapped_column(Numeric(10, 3), nullable=False)
    mat_fornecedor: Mapped[str] = mapped_column(String(90), nullable=False)
    mat_validade: Mapped[date] = mapped_column(Date, nullable=False)
    mat_lab_id: Mapped[int] = mapped_column(ForeignKey('tb_laboratorios.lab_id'), nullable=False)
    mat_cat_id: Mapped[int] = mapped_column(ForeignKey('tb_categorias_materiais.cat_id'), nullable=False)

    laboratorio = relationship('Lab', back_populates='materiais', lazy=True)
    categoria = relationship('CategoriaMaterial', back_populates='materiais', lazy=True)
    reservas_materiais = relationship('ReservaMaterial', back_populates='material', lazy=True)

    def __repr__(self):
        return f'Material {self.mat_nome} - Quantidade: {self.mat_quantidade}'

    def __init__(self, nome, descricao, quantidade, fornecedor, validade, lab_id, cat_id) -> None:
        self.mat_nome = nome
        self.mat_quantidade = quantidade
        self.mat_descricao = descricao
        self.mat_fornecedor = fornecedor
        self.mat_validade = validade
        self.mat_lab_id = lab_id
        self.mat_cat_id = cat_id

class Reagente(db.Model):
    __tablename__ = 'tb_reagentes'

    rgt_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rgt_nome: Mapped[str] = mapped_column(String(50), nullable=False)
    rgt_quantidade: Mapped[DECIMAL] = mapped_column(Numeric(10, 3), nullable=False)
    rgt_unidade: Mapped[Enum] = mapped_column(Enum('g', 'l'), nullable=False)
    rgt_fornecedor: Mapped[str] = mapped_column(String(90), nullable=False)
    rgt_validade: Mapped[date] = mapped_column(Date, nullable=False)
    rgt_lab_id: Mapped[int] = mapped_column(ForeignKey('tb_laboratorios.lab_id'), nullable=False)
    rgt_cat_id: Mapped[int] = mapped_column(ForeignKey('tb_categorias_reagentes.cat_id'), nullable=False)

    laboratorio = relationship('Lab', back_populates='reagentes', lazy=True)
    categoria = relationship('CategoriaReagente', back_populates='reagentes', lazy=True)
    reservas_reagentes = relationship('ReservaReagente', back_populates='reagente', lazy=True)

    def __repr__(self):
        return f'Reagente {self.rgt_nome} - Quantidade: {self.rgt_quantidade}'

    def __init__(self, nome, quantidade, unidade, fornecedor, validade, lab_id, cat_id) -> None:
        self.rgt_nome = nome
        self.rgt_quantidade = quantidade
        self.rgt_unidade = unidade
        self.rgt_fornecedor = fornecedor
        self.rgt_validade = validade
        self.rgt_lab_id = lab_id
        self.rgt_cat_id = cat_id

class ReservaItens(db.Model):
    __tablename__ = 'tb_reservas_itens'

    rei_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rei_rel_id: Mapped[int] = mapped_column(ForeignKey('tb_reservas_laboratorios.rel_id'), nullable=False)

    reserva_lab = relationship('ReservaLab', back_populates='reserva_itens')
    materiais_reservados = relationship('ReservaMaterial', back_populates='reserva_itens', lazy=True)
    reagentes_reservados = relationship('ReservaReagente', back_populates='reserva_itens', lazy=True)

    def __repr__(self):
        return f"<ReservaItens id={self.rei_id} reserva_laboratorio_id={self.rei_rel_id}>"

    def __init__(self, rel_id) -> None:
        self.rei_rel_id = rel_id

class ReservaMaterial(db.Model):
    __tablename__ = 'tb_reservas_materiais'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    material_id: Mapped[int] = mapped_column(ForeignKey('tb_materiais.mat_id'), nullable=False)
    reserva_itens_id: Mapped[int] = mapped_column(ForeignKey('tb_reservas_itens.rei_id'), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)

    material = relationship('Material', back_populates='reservas_materiais')
    reserva_itens = relationship('ReservaItens', back_populates='materiais_reservados')

    def __repr__(self):
        return f"<ReservaMaterial material_id={self.material_id} reserva_itens_id={self.reserva_itens_id}>"

class ReservaReagente(db.Model):
    __tablename__ = 'tb_reservas_reagentes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reagente_id: Mapped[int] = mapped_column(ForeignKey('tb_reagentes.rgt_id'), nullable=False)
    reserva_itens_id: Mapped[int] = mapped_column(ForeignKey('tb_reservas_itens.rei_id'), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    unidade: Mapped[str] = mapped_column(String(2), nullable=False)

    reagente = relationship('Reagente', back_populates='reservas_reagentes')
    reserva_itens = relationship('ReservaItens', back_populates='reagentes_reservados')

    def __repr__(self):
        return f"<ReservaReagente reagente_id={self.reagente_id} reserva_itens_id={self.reserva_itens_id}>"