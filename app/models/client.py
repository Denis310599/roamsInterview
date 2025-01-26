from app.models import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime


class Client(db.Model):
  dni: so.Mapped[str] = so.mapped_column(sa.String(9), primary_key=True)
  nombre: so.Mapped[str] = so.mapped_column(sa.String(80), nullable=False)
  email: so.Mapped[str] = so.mapped_column(sa.String(120), nullable=False)
  capital_solicitado: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)


class User(db.Model):
  username: so.Mapped[str] = so.mapped_column(sa.String(80), nullable=False, primary_key=True)
  passwd: so.Mapped[str] = so.mapped_column(sa.String(120), nullable=False)


class Simulation(db.Model):
  id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True, autoincrement=True)
  dni: so.Mapped[str] =  so.mapped_column(sa.String(9))
  fecha_simulacion: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=False, default=datetime.now())
  capital: so.Mapped[float] = so.mapped_column(nullable=False)
  tae: so.Mapped[float] = so.mapped_column(sa.Float)
  plazo_amortizacion: so.Mapped[int] = so.mapped_column(sa.Integer)
  cuota_mensual: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
  importe_devolver: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
