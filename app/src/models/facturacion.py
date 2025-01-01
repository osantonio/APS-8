from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Text, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from .residentes import Residente
from .inventario import Suministro
import enum

class EstadoFactura(enum.Enum):
    PENDIENTE = "pendiente"
    PAGADA = "pagada"
    VENCIDA = "vencida"
    CANCELADA = "cancelada"

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False)
    fecha_emision = Column(DateTime(timezone=True), server_default=func.now())
    fecha_vencimiento = Column(DateTime(timezone=True), nullable=False)
    estado = Column(String(20), nullable=False, default=EstadoFactura.PENDIENTE.value)
    total = Column(Numeric(10, 2), nullable=False)
    notas = Column(Text)

    # Relaciones
    residente = relationship("Residente", back_populates="facturas")
    detalles = relationship("DetalleFactura", back_populates="factura")

class DetalleFactura(Base):
    __tablename__ = "detalles_factura"

    id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    suministro_id = Column(Integer, ForeignKey("suministros.id"), nullable=False)
    cantidad = Column(Numeric(10, 2), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    # Relaciones
    factura = relationship("Factura", back_populates="detalles")
    suministro = relationship("Suministro")
