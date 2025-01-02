from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
import os
import logging

# Configurar los registros de SQLAlchemy para reducir la verbosidad
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)

# Obtener la ruta absoluta al directorio actual
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Crear el motor de base de datos SQLite asíncrono
SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(BASE_DIR, 'aps.db')}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

# Crear la sesión asíncrona
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Crear la base para los modelos
Base = declarative_base()

# Función para obtener la sesión de base de datos
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependencia para obtener una sesión de base de datos asíncrona.
    
    Esta función crea un generador asíncrono que:
    1. Crea una nueva sesión de base de datos
    2. Yield la sesión para su uso en los endpoints
    3. Asegura que la sesión se cierre correctamente después de su uso
    
    Uso en FastAPI:
        @app.get("/items")
        async def read_items(db: AsyncSession = Depends(get_db)):
            ...
    
    Returns:
        AsyncSession: Sesión asíncrona de SQLAlchemy
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # Intentar commit de la transacción si no ha habido errores
            await session.commit()
        except Exception:
            # Rollback en caso de error
            await session.rollback()
            raise
        finally:
            # Asegurar que la sesión se cierre
            await session.close()

# Función para eliminar todas las tablas
async def drop_tables():
    """
    Elimina todas las tablas de la base de datos.
    ¡PRECAUCIÓN! Esta función eliminará todos los datos.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Función para crear todas las tablas
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
