from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import AsyncGenerator, Generator
from sqlalchemy.pool import StaticPool
import os
import logging

# Importaciones adicionales para manejar rutas
from pathlib import Path

# Obtener la ruta absoluta al directorio actual
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'aps.db'

# Asegurar que el directorio de la base de datos exista
os.makedirs(DB_PATH.parent, exist_ok=True)

# Crear el motor de base de datos SQLite asíncrono
SQLALCHEMY_DATABASE_URL_ASYNC = f"sqlite+aiosqlite:///{DB_PATH}"
SQLALCHEMY_DATABASE_URL_SYNC = f"sqlite:///{DB_PATH}"

# Motor asíncrono
engine_async = create_async_engine(
    SQLALCHEMY_DATABASE_URL_ASYNC,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

# Motor síncrono
engine_sync = create_engine(
    SQLALCHEMY_DATABASE_URL_SYNC,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Crear la sesión asíncrona
AsyncSessionLocal = async_sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Crear la sesión síncrona
SessionLocal = sessionmaker(
    bind=engine_sync,
    autocommit=False,
    autoflush=False
)

# Crear la base para los modelos
Base = declarative_base()

# Función para obtener la sesión de base de datos asíncrona
async def get_db_async() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Función para obtener la sesión de base de datos síncrona
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# Función para eliminar todas las tablas
async def drop_tables():
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Función para crear todas las tablas
async def create_tables():
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
