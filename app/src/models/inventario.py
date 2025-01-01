from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class CategoriaProducto(enum.Enum):
    MEDICAMENTO = "medicamento"
    MATERIAL_CURACION = "material_curacion"
    LIMPIEZA = "limpieza"
    ALIMENTOS = "alimentos"
    PAPELERIA = "papeleria"
    ROPA_CAMA = "ropa_cama"
    EQUIPO_MEDICO = "equipo_medico"
    OTROS = "otros"

class UnidadMedida(enum.Enum):
    PIEZA = "pieza"
    CAJA = "caja"
    PAQUETE = "paquete"
    KILOGRAMO = "kilogramo"
    LITRO = "litro"
    GRAMO = "gramo"
    MILILITRO = "mililitro"

class EstadoSuministro(enum.Enum):
    PENDIENTE = "pendiente"
    PROCESANDO = "procesando"
    ENVIADO = "enviado"
    RECIBIDO = "recibido"
    CANCELADO = "cancelado"

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    categoria = Column(Enum(CategoriaProducto), nullable=False)
    unidad_medida = Column(Enum(UnidadMedida), nullable=False)
    stock_actual = Column(Float, default=0)
    stock_minimo = Column(Float, nullable=False)
    ubicacion = Column(String(100))
    notas = Column(Text)
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relación con suministros
    suministros = relationship("Suministro", back_populates="producto")

class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    tipo_movimiento = Column(String(20), nullable=False)  # entrada, salida
    cantidad = Column(Float, nullable=False)
    fecha_movimiento = Column(DateTime(timezone=True), server_default=func.now())
    responsable = Column(String(200), nullable=False)
    motivo = Column(Text, nullable=False)
    documento_referencia = Column(String(100))  # número de factura, remisión, etc.
    notas = Column(Text)

class Suministro(Base):
    __tablename__ = "suministros"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad_solicitada = Column(Float, nullable=False)
    cantidad_recibida = Column(Float, default=0)
    estado = Column(Enum(EstadoSuministro), nullable=False, default=EstadoSuministro.PENDIENTE)
    proveedor = Column(String(200), nullable=False)
    fecha_solicitud = Column(DateTime(timezone=True), server_default=func.now())
    fecha_entrega_estimada = Column(DateTime(timezone=True))
    fecha_entrega_real = Column(DateTime(timezone=True))
    costo_unitario = Column(Float)
    total = Column(Float)
    urgente = Column(Boolean, default=False)
    notas = Column(Text)

    # Relación con producto
    producto = relationship("Producto", back_populates="suministros")
