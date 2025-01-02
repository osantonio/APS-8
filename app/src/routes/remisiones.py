from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime

from ..models import (
    Remision, 
    SeguimientoRemision, 
    TrazabilidadProfesional,
    TipoRemision, 
    EstadoRemision, 
    TipoEvento,
    Residente,
    Colaborador
)
from ..models.database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

# Modelos de Solicitud/Respuesta
class RemisionBase(BaseModel):
    numero_remision: str
    residente_id: int
    tipo: TipoRemision
    estado: Optional[EstadoRemision] = EstadoRemision.PROGRAMADA
    institucion_destino: str
    direccion_destino: str
    medico_receptor: Optional[str] = None
    especialidad: Optional[str] = None
    fecha_programada: datetime
    motivo: str
    diagnostico_envio: str
    medico_remitente: str

class RemisionCreate(RemisionBase):
    pass

class RemisionUpdate(BaseModel):
    estado: Optional[EstadoRemision] = None
    fecha_salida: Optional[datetime] = None
    fecha_retorno: Optional[datetime] = None
    notas_seguimiento: Optional[str] = None

class SeguimientoRemisionBase(BaseModel):
    remision_id: int
    tipo_evento: TipoEvento
    fecha_hora: datetime
    ubicacion: Optional[str] = None
    descripcion: Optional[str] = None
    responsable: Optional[str] = None
    observaciones: Optional[str] = None

class SeguimientoRemisionCreate(SeguimientoRemisionBase):
    pass

class TrazabilidadProfesionalBase(BaseModel):
    remision_id: int
    colaborador_id: int
    rol: str
    fecha_intervencion: datetime
    descripcion_intervencion: Optional[str] = None
    notas: Optional[str] = None
    documentos_generados: Optional[str] = None

class TrazabilidadProfesionalCreate(TrazabilidadProfesionalBase):
    pass

# Router
router = APIRouter(prefix="/remisiones", tags=["Remisiones"])

# Endpoints existentes de remisiones (sin cambios)
@router.post("/", response_model=RemisionBase)
async def crear_remision(remision: RemisionCreate, db: AsyncSession = Depends(get_db)):
    # Verificar que el residente exista
    result = await db.execute(select(Residente).filter(Residente.id == remision.residente_id))
    residente = result.scalar_one_or_none()
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")

    # Generar número de remisión único
    result = await db.execute(select(Remision))
    total_remisiones = len(result.scalars().all())
    nuevo_numero = f"REM-{datetime.now().strftime('%Y%m%d')}-{total_remisiones + 1:04d}"
    
    db_remision = Remision(
        numero_remision=nuevo_numero,
        **remision.dict()
    )
    
    db.add(db_remision)
    await db.commit()
    await db.refresh(db_remision)
    
    return db_remision

# Nuevos endpoints para trazabilidad de profesionales
@router.post("/{remision_id}/trazabilidad", response_model=TrazabilidadProfesionalBase)
async def agregar_trazabilidad_profesional(
    remision_id: int, 
    trazabilidad: TrazabilidadProfesionalCreate, 
    db: AsyncSession = Depends(get_db)
):
    # Verificar que la remisión exista
    result = await db.execute(select(Remision).filter(Remision.id == remision_id))
    remision = result.scalar_one_or_none()
    if not remision:
        raise HTTPException(status_code=404, detail="Remisión no encontrada")

    # Verificar que el colaborador exista
    result = await db.execute(select(Colaborador).filter(Colaborador.id == trazabilidad.colaborador_id))
    colaborador = result.scalar_one_or_none()
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")

    db_trazabilidad = TrazabilidadProfesional(
        remision_id=remision_id,
        **trazabilidad.dict(exclude={'remision_id'})
    )
    
    db.add(db_trazabilidad)
    await db.commit()
    await db.refresh(db_trazabilidad)
    
    return db_trazabilidad

@router.get("/{remision_id}/trazabilidad", response_model=List[TrazabilidadProfesionalBase])
async def listar_trazabilidad_profesional(remision_id: int, db: AsyncSession = Depends(get_db)):
    # Verificar que la remisión exista
    result = await db.execute(select(Remision).filter(Remision.id == remision_id))
    remision = result.scalar_one_or_none()
    if not remision:
        raise HTTPException(status_code=404, detail="Remisión no encontrada")

    result = await db.execute(
        select(TrazabilidadProfesional).filter(TrazabilidadProfesional.remision_id == remision_id)
    )
    trazabilidades = result.scalars().all()
    
    return trazabilidades

# Endpoints existentes (sin cambios)
@router.get("/", response_model=List[RemisionBase])
async def listar_remisiones(
    estado: Optional[EstadoRemision] = None, 
    tipo: Optional[TipoRemision] = None, 
    db: AsyncSession = Depends(get_db)
):
    query = select(Remision)
    
    if estado:
        query = query.filter(Remision.estado == estado)
    
    if tipo:
        query = query.filter(Remision.tipo == tipo)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{remision_id}", response_model=RemisionBase)
async def obtener_remision(remision_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Remision).filter(Remision.id == remision_id))
    remision = result.scalar_one_or_none()
    
    if not remision:
        raise HTTPException(status_code=404, detail="Remisión no encontrada")
    
    return remision

@router.put("/{remision_id}", response_model=RemisionBase)
async def actualizar_remision(
    remision_id: int, 
    remision_update: RemisionUpdate, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Remision).filter(Remision.id == remision_id))
    db_remision = result.scalar_one_or_none()
    
    if not db_remision:
        raise HTTPException(status_code=404, detail="Remisión no encontrada")
    
    for key, value in remision_update.dict(exclude_unset=True).items():
        setattr(db_remision, key, value)
    
    await db.commit()
    await db.refresh(db_remision)
    
    return db_remision

@router.post("/{remision_id}/seguimiento", response_model=SeguimientoRemisionBase)
async def agregar_seguimiento(
    remision_id: int, 
    seguimiento: SeguimientoRemisionCreate, 
    db: AsyncSession = Depends(get_db)
):
    # Verificar que la remisión exista
    result = await db.execute(select(Remision).filter(Remision.id == remision_id))
    remision = result.scalar_one_or_none()
    if not remision:
        raise HTTPException(status_code=404, detail="Remisión no encontrada")

    db_seguimiento = SeguimientoRemision(
        **seguimiento.dict()
    )
    
    db.add(db_seguimiento)
    await db.commit()
    await db.refresh(db_seguimiento)
    
    return db_seguimiento

@router.get("/{remision_id}/seguimiento", response_model=List[SeguimientoRemisionBase])
async def listar_seguimientos(remision_id: int, db: AsyncSession = Depends(get_db)):
    # Verificar que la remisión exista
    result = await db.execute(select(Remision).filter(Remision.id == remision_id))
    remision = result.scalar_one_or_none()
    if not remision:
        raise HTTPException(status_code=404, detail="Remisión no encontrada")

    result = await db.execute(
        select(SeguimientoRemision).filter(SeguimientoRemision.remision_id == remision_id)
    )
    seguimientos = result.scalars().all()
    
    return seguimientos
