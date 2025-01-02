from .database import Base, engine_sync as engine, get_db, create_tables
from .colaboradores import Colaborador, TipoColaborador
from .residentes import Residente, TipoSangre, EstadoResidente
from .inventario import Producto, MovimientoInventario, CategoriaProducto, UnidadMedida
from .remisiones import (
    Remision, 
    TipoRemision, 
    EstadoRemision, 
    SeguimientoRemision, 
    TipoEvento,
    TrazabilidadProfesional
)

__all__ = [
    # Database
    "Base",
    "engine",
    "get_db",
    "create_tables",
    
    # Colaboradores
    "Colaborador",
    "TipoColaborador",
    
    # Residentes
    "Residente",
    "TipoSangre",
    "EstadoResidente",
    
    # Inventario
    "Producto",
    "MovimientoInventario",
    "CategoriaProducto",
    "UnidadMedida",
    
    # Remisiones
    "Remision",
    "TipoRemision",
    "EstadoRemision",
    "SeguimientoRemision",
    "TipoEvento",
    "TrazabilidadProfesional",
]
