from sqlalchemy import Integer, String, Date, Time, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import db
from datetime import datetime, date, time

class Aula(db.Model):
    __tablename__ = 'tb_aulas'

    aul_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    aul_titulo: Mapped[str] = mapped_column(String(50), nullable=False)
    aul_desc: Mapped[str] = mapped_column(String(300), nullable=False)
    aul_horarioInicio: Mapped[str] = mapped_column(Time, nullable=False)
    aul_horarioTermino: Mapped[str] = mapped_column(Time, nullable=False)
    aul_data: Mapped[str] = mapped_column(Date, nullable=False)

    aul_lab_id: Mapped[int] = mapped_column(ForeignKey('tb_laboratorios.lab_id'), nullable=False)
    aul_usu_id: Mapped[int] = mapped_column(ForeignKey('tb_usuarios.usu_matricula'), nullable=False)

    laboratorio = relationship('Lab', back_populates='aulas', lazy=True)

    def __repr__(self):
        return f"<Aula id={self.aul_id}, titulo='{self.aul_titulo}', data={self.aul_data}>"
