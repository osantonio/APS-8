from sqlalchemy import Column, Integer, String, Boolean, Date, Enum
from .database import Base
import enum
import hashlib
import secrets

class TipoColaborador(enum.Enum):
    ENFERMERO = "enfermero"
    MEDICO = "medico"
    ADMINISTRATIVO = "administrativo"
    LIMPIEZA = "limpieza"
    COCINA = "cocina"
    MANTENIMIENTO = "mantenimiento"

class RolAcceso(enum.Enum):
    ADMIN = "admin"
    COLABORADOR = "colaborador"

class Colaborador(Base):
    __tablename__ = "colaboradores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100))
    fecha_nacimiento = Column(Date, nullable=False)
    tipo = Column(Enum(TipoColaborador), nullable=False)
    telefono = Column(String(15))
    correo = Column(String(100), unique=True, nullable=False)
    direccion = Column(String(200))
    activo = Column(Boolean, default=True)
    fecha_ingreso = Column(Date, nullable=False)
    numero_empleado = Column(String(20), unique=True, nullable=False)
    turno = Column(String(20), nullable=False)  # Matutino, Vespertino, Nocturno
    
    # Nuevos campos para autenticación
    contrasena = Column(String(255), nullable=False)
    rol = Column(Enum(RolAcceso), nullable=False)

    def verificar_contrasena(self, contrasena_ingresada):
        # Hashear la contraseña ingresada y comparar
        salt, hash_guardado = self.contrasena.split('$')
        hash_ingresado = hashlib.pbkdf2_hmac(
            'sha256', 
            contrasena_ingresada.encode(), 
            salt.encode(), 
            100000
        ).hex()
        return hash_ingresado == hash_guardado

    @staticmethod
    def hashear_contrasena(contrasena):
        # Método estático para hashear contraseñas con salt
        salt = secrets.token_hex(16)  # Generar un salt aleatorio
        hash_contrasena = hashlib.pbkdf2_hmac(
            'sha256', 
            contrasena.encode(), 
            salt.encode(), 
            100000
        ).hex()
        return f"{salt}${hash_contrasena}"
