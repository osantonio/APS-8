from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from datetime import datetime, timedelta

from ..models.database import get_db
from ..models.facturacion import Factura, DetalleFactura, EstadoFactura
from ..models.residentes import Residente
from ..models.inventario import Suministro

from pydantic import BaseModel, validator

router = APIRouter(
    prefix="/facturacion",
    tags=["facturacion"],
    responses={404: {"description": "No encontrado"}}
)

class DetalleFacturaBase(BaseModel):
    suministro_id: int
    cantidad: Decimal
    precio_unitario: Decimal

class FacturaCreate(BaseModel):
    residente_id: int
    detalles: List[DetalleFacturaBase]
    fecha_vencimiento: Optional[datetime] = None
    notas: Optional[str] = None

    @validator('fecha_vencimiento', always=True)
    def set_default_vencimiento(cls, v):
        return v or datetime.now() + timedelta(days=30)

class FacturaResponse(BaseModel):
    id: int
    residente_id: int
    fecha_emision: datetime
    fecha_vencimiento: datetime
    estado: str
    total: Decimal
    notas: Optional[str]

    class Config:
        orm_mode = True

@router.post("/", response_model=FacturaResponse, status_code=status.HTTP_201_CREATED)
async def crear_factura(factura: FacturaCreate, db: Session = Depends(get_db)):
    # Verificar que el residente existe
    residente = db.query(Residente).filter(Residente.id == factura.residente_id).first()
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")
    
    # Calcular total de la factura
    total = Decimal('0')
    detalles_factura = []

    for detalle in factura.detalles:
        # Verificar que el suministro existe
        suministro = db.query(Suministro).filter(Suministro.id == detalle.suministro_id).first()
        if not suministro:
            raise HTTPException(status_code=404, detail=f"Suministro {detalle.suministro_id} no encontrado")
        
        subtotal = detalle.cantidad * detalle.precio_unitario
        total += subtotal

        detalles_factura.append(DetalleFactura(
            suministro_id=detalle.suministro_id,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario,
            subtotal=subtotal
        ))

    # Crear factura
    nueva_factura = Factura(
        residente_id=factura.residente_id,
        fecha_vencimiento=factura.fecha_vencimiento,
        total=total,
        notas=factura.notas,
        estado=EstadoFactura.PENDIENTE.value
    )

    try:
        db.add(nueva_factura)
        db.flush()  # Obtener el ID de la factura

        # Asociar detalles a la factura
        for detalle in detalles_factura:
            detalle.factura_id = nueva_factura.id
            db.add(detalle)

        db.commit()
        db.refresh(nueva_factura)
        return nueva_factura

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear la factura: {str(e)}"
        )

@router.get("/", response_model=List[FacturaResponse])
async def listar_facturas(
    skip: int = 0,
    limit: int = 100,
    residente_id: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Factura)
    
    if residente_id:
        query = query.filter(Factura.residente_id == residente_id)
    
    if estado:
        # Validar que el estado sea uno de los valores permitidos
        if estado not in [e.value for e in EstadoFactura]:
            raise HTTPException(status_code=400, detail="Estado de factura inválido")
        query = query.filter(Factura.estado == estado)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{factura_id}", response_model=FacturaResponse)
async def obtener_factura(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

@router.put("/{factura_id}/estado", response_model=FacturaResponse)
async def actualizar_estado_factura(
    factura_id: int, 
    estado: str,
    db: Session = Depends(get_db)
):
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    # Validar que el estado sea uno de los valores permitidos
    if estado not in [e.value for e in EstadoFactura]:
        raise HTTPException(status_code=400, detail="Estado de factura inválido")
    
    try:
        # Usar update para evitar problemas de asignación
        db.query(Factura).filter(Factura.id == factura_id).update({"estado": estado})
        db.commit()
        db.refresh(factura)
        return factura
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error al actualizar el estado de la factura: {str(e)}"
        )

@router.delete("/{factura_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_factura(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    try:
        db.delete(factura)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error al eliminar la factura: {str(e)}"
        )
