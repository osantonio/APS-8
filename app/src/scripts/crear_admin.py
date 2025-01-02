import sys
import os
import traceback
from datetime import date

# Obtener la ruta absoluta del directorio raíz del proyecto
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from src.models.database import engine_sync, Base, DB_PATH
from src.models.colaboradores import Colaborador, RolAcceso, TipoColaborador

# Configurar logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_sync)

def crear_usuario_admin():
    # Crear sesión de base de datos
    db = SessionLocal()
    
    try:
        # Listar todos los usuarios existentes
        usuarios_existentes = db.query(Colaborador).all()
        logger.info(f"Usuarios existentes: {len(usuarios_existentes)}")
        for usuario in usuarios_existentes:
            logger.info(f"Usuario: {usuario.nombre} {usuario.apellido_paterno}, Correo: {usuario.correo}, Rol: {usuario.rol}")
        
        # Verificar si ya existe un admin
        admin_existente = db.query(Colaborador).filter(
            Colaborador.rol == RolAcceso.ADMIN
        ).first()
        
        if admin_existente:
            logger.info("Ya existe un usuario administrador.")
            return
        
        # Crear nuevo usuario admin
        nuevo_admin = Colaborador(
            nombre="Administrador",
            apellido_paterno="Principal",
            apellido_materno="Sistema",
            fecha_nacimiento=date(1990, 1, 1),
            tipo=TipoColaborador.ADMINISTRATIVO,
            telefono="5555555555",
            correo="admin@asilo.com",
            direccion="Dirección del Asilo",
            activo=True,
            fecha_ingreso=date.today(),
            numero_empleado="ADMIN001",
            turno="Completo",
            rol=RolAcceso.ADMIN,
            contrasena=Colaborador.hashear_contrasena("AdminAPS2023!")
        )
        
        db.add(nuevo_admin)
        db.commit()
        logger.info("Usuario administrador creado exitosamente.")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear usuario administrador: {e}")
        logger.error(traceback.format_exc())
    finally:
        db.close()

def verificar_tablas():
    # Verificar las tablas existentes
    inspector = inspect(engine_sync)
    tablas = inspector.get_table_names()
    logger.info(f"Tablas existentes: {tablas}")

if __name__ == "__main__":
    # Información de depuración
    logger.info(f"Ruta de la base de datos: {DB_PATH}")
    logger.info(f"Directorio de la base de datos existe: {os.path.exists(DB_PATH.parent)}")
    
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine_sync)
    
    # Verificar tablas
    verificar_tablas()
    
    # Crear usuario admin
    crear_usuario_admin()
