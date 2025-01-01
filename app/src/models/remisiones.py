from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class TipoRemision(enum.Enum):
    CONSULTA = "consulta"
    EMERGENCIA = "emergencia"
    HOSPITALIZACION = "hospitalizacion"
    ESTUDIOS = "estudios"
    TRASLADO = "traslado"

class EstadoRemision(enum.Enum):
    PROGRAMADA = "programada"
    EN_PROCESO = "en_proceso"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"

class Remision(Base):
    __tablename__ = "remisiones"

    id = Column(Integer, primary_key=True, index=True)
    numero_remision = Column(String(20), unique=True, nullable=False)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False)
    tipo = Column(Enum(TipoRemision), nullable=False)
    estado = Column(Enum(EstadoRemision), default=EstadoRemision.PROGRAMADA)
    
    # Información del destino
    institucion_destino = Column(String(200), nullable=False)
    direccion_destino = Column(String(200), nullable=False)
    medico_receptor = Column(String(200))
    especialidad = Column(String(100))
    
    # Fechas
    fecha_programada = Column(DateTime(timezone=True), nullable=False)
    fecha_salida = Column(DateTime(timezone=True))
    fecha_retorno = Column(DateTime(timezone=True))
    
    # Información médica
    motivo = Column(Text, nullable=False)
    diagnostico_envio = Column(Text, nullable=False)
    signos_vitales = Column(Text)
    indicaciones = Column(Text)
    
    # Documentación
    documentos_adjuntos = Column(Text)  # Lista de documentos necesarios
    estudios_solicitados = Column(Text)
    
    # Personal responsable
    medico_remitente = Column(String(200), nullable=False)
    enfermero_acompanante = Column(String(200))
    familiar_acompanante = Column(String(200))
    
    # Transporte
    requiere_ambulancia = Column(Boolean, default=False)
    tipo_transporte = Column(String(100))
    empresa_transporte = Column(String(200))
    
    # Seguimiento
    notas_seguimiento = Column(Text)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Costos
    costo_estimado = Column(Float)
    gastos_adicionales = Column(Text)  # Registro de gastos no previstos
    
    # Relaciones
    residente = relationship("Residente", backref="remisiones")
