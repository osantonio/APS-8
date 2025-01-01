from sqlalchemy import Column, Integer, String, Boolean, Date, Enum
from .database import Base
import enum

class TipoColaborador(enum.Enum):
    ENFERMERO = "enfermero"
    MEDICO = "medico"
    ADMINISTRATIVO = "administrativo"
    LIMPIEZA = "limpieza"
    COCINA = "cocina"
    MANTENIMIENTO = "mantenimiento"

class Colaborador(Base):
    __tablename__ = "colaboradores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100))
    fecha_nacimiento = Column(Date, nullable=False)
    tipo = Column(Enum(TipoColaborador), nullable=False)
    telefono = Column(String(15))
    correo = Column(String(100))
    direccion = Column(String(200))
    activo = Column(Boolean, default=True)
    fecha_ingreso = Column(Date, nullable=False)
    numero_empleado = Column(String(20), unique=True, nullable=False)
    turno = Column(String(20), nullable=False)  # Matutino, Vespertino, Nocturno
