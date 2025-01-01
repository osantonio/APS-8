from sqlalchemy import Column, Integer, String, Date, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class TipoSangre(enum.Enum):
    A_POSITIVO = "A+"
    A_NEGATIVO = "A-"
    B_POSITIVO = "B+"
    B_NEGATIVO = "B-"
    AB_POSITIVO = "AB+"
    AB_NEGATIVO = "AB-"
    O_POSITIVO = "O+"
    O_NEGATIVO = "O-"

class EstadoResidente(enum.Enum):
    ACTIVO = "activo"
    HOSPITALIZADO = "hospitalizado"
    AUSENTE_TEMPORAL = "ausente_temporal"
    INACTIVO = "inactivo"

class Residente(Base):
    __tablename__ = "residentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100))
    fecha_nacimiento = Column(Date, nullable=False)
    fecha_ingreso = Column(Date, nullable=False)
    tipo_sangre = Column(Enum(TipoSangre), nullable=False)
    estado = Column(Enum(EstadoResidente), default=EstadoResidente.ACTIVO)
    
    # Información médica
    alergias = Column(Text)
    condiciones_medicas = Column(Text)
    medicamentos = Column(Text)
    dieta_especial = Column(Text)
    nivel_movilidad = Column(String(50))
    
    # Contacto de emergencia
    contacto_emergencia_nombre = Column(String(200), nullable=False)
    contacto_emergencia_relacion = Column(String(100), nullable=False)
    contacto_emergencia_telefono = Column(String(15), nullable=False)
    contacto_emergencia_direccion = Column(String(200))
    
    # Información administrativa
    numero_expediente = Column(String(20), unique=True, nullable=False)
    seguro_medico = Column(String(100))
    numero_seguro = Column(String(50))
    activo = Column(Boolean, default=True)
    notas = Column(Text)
