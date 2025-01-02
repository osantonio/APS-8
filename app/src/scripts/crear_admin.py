import sys
import os

# Agregar el directorio padre al path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.database import Base
import os

# Crear motor de base de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'app', 'src', 'aps.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Asegurar que el directorio exista
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Importar Base para crear tablas si no existen
from src.models.database import Base
Base.metadata.create_all(bind=engine)

from src.models.colaboradores import Colaborador, RolAcceso, TipoColaborador
from datetime import date

def crear_usuario_admin():
    # Imprimir información de depuración
    print(f"Ruta de la base de datos: {DB_PATH}")
    print(f"Directorio base: {BASE_DIR}")
    print(f"Contenido del directorio: {os.listdir(os.path.dirname(DB_PATH))}")
    
    # Crear sesión de base de datos
    db = SessionLocal()
    
    try:
        # Verificar si ya existe un admin
        admin_existente = db.query(Colaborador).filter(
            Colaborador.rol == RolAcceso.ADMIN
        ).first()
        
        if admin_existente:
            print("Ya existe un usuario administrador.")
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
        print("Usuario administrador creado exitosamente.")
    
    except Exception as e:
        db.rollback()
        print(f"Error al crear usuario administrador: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    crear_usuario_admin()
