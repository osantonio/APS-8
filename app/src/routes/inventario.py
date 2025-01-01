from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.database import get_db
from ..models.inventario import (
    Producto, 
    MovimientoInventario, 
    Suministro, 
    CategoriaProducto, 
    UnidadMedida, 
    EstadoSuministro
)
from pydantic import BaseModel, Field, validator
from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional

router = APIRouter(
    prefix="/inventario",
    tags=["inventario"],
    responses={404: {"description": "No encontrado"}}
)

# Esquemas Pydantic para validación de datos
class ProductoBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    categoria: CategoriaProducto
    unidad_medida: UnidadMedida
    stock_minimo: Decimal
    ubicacion: Optional[str] = None
    notas: Optional[str] = None

    @validator('codigo')
    def validar_codigo(cls, v):
        if not (1 <= len(v) <= 50):
            raise ValueError('El código debe tener entre 1 y 50 caracteres')
        return v

    @validator('nombre')
    def validar_nombre(cls, v):
        if not (1 <= len(v) <= 200):
            raise ValueError('El nombre debe tener entre 1 y 200 caracteres')
        return v

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[CategoriaProducto] = None
    unidad_medida: Optional[UnidadMedida] = None
    stock_minimo: Optional[Decimal] = None
    ubicacion: Optional[str] = None
    notas: Optional[str] = None

    @validator('codigo')
    def validar_codigo(cls, v):
        if v is not None and not (1 <= len(v) <= 50):
            raise ValueError('El código debe tener entre 1 y 50 caracteres')
        return v

    @validator('nombre')
    def validar_nombre(cls, v):
        if v is not None and not (1 <= len(v) <= 200):
            raise ValueError('El nombre debe tener entre 1 y 200 caracteres')
        return v

class MovimientoBase(BaseModel):
    producto_id: int
    tipo_movimiento: Literal["entrada", "salida"]
    cantidad: Decimal
    responsable: str
    motivo: str
    documento_referencia: Optional[str] = None
    notas: Optional[str] = None

    @validator('responsable')
    def validar_responsable(cls, v):
        if not (1 <= len(v) <= 200):
            raise ValueError('El responsable debe tener entre 1 y 200 caracteres')
        return v

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }

class MovimientoCreate(MovimientoBase):
    pass

# Nuevos esquemas para Suministro
class SuministroBase(BaseModel):
    producto_id: int
    cantidad_solicitada: Decimal
    cantidad_recibida: Optional[Decimal] = Decimal('0')
    estado: EstadoSuministro = EstadoSuministro.PENDIENTE
    proveedor: str
    fecha_entrega_estimada: Optional[datetime] = None
    costo_unitario: Optional[Decimal] = None
    total: Optional[Decimal] = None
    urgente: bool = False
    notas: Optional[str] = None

    @validator('proveedor')
    def validar_proveedor(cls, v):
        if not (1 <= len(v) <= 200):
            raise ValueError('El nombre del proveedor debe tener entre 1 y 200 caracteres')
        return v

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }

class SuministroCreate(SuministroBase):
    pass

class SuministroUpdate(BaseModel):
    cantidad_solicitada: Optional[Decimal] = None
    cantidad_recibida: Optional[Decimal] = None
    estado: Optional[EstadoSuministro] = None
    proveedor: Optional[str] = None
    fecha_entrega_estimada: Optional[datetime] = None
    fecha_entrega_real: Optional[datetime] = None
    costo_unitario: Optional[Decimal] = None
    total: Optional[Decimal] = None
    urgente: Optional[bool] = None
    notas: Optional[str] = None

# Endpoints para Productos
@router.post("/productos/", response_model=ProductoBase, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    try:
        db.commit()
        db.refresh(db_producto)
        return db_producto
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear el producto: {str(e)}"
        )

@router.get("/productos/", response_model=List[ProductoBase])
async def listar_productos(
    skip: int = 0,
    limit: int = 100,
    categoria: Optional[CategoriaProducto] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Producto)
    if categoria:
        query = query.filter(Producto.categoria == categoria)
    return query.offset(skip).limit(limit).all()

@router.get("/productos/{producto_id}", response_model=ProductoBase)
async def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/productos/{producto_id}", response_model=ProductoBase)
async def actualizar_producto(
    producto_id: int,
    producto_update: ProductoUpdate,
    db: Session = Depends(get_db)
):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    update_data = producto_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_producto, field, value)
    
    try:
        db.commit()
        db.refresh(db_producto)
        return db_producto
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error al actualizar el producto: {str(e)}"
        )

@router.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    try:
        db.delete(producto)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error al eliminar el producto: {str(e)}"
        )

# Endpoints para Movimientos de Inventario
@router.post("/movimientos/", response_model=MovimientoBase, status_code=status.HTTP_201_CREATED)
async def registrar_movimiento(movimiento: MovimientoCreate, db: Session = Depends(get_db)):
    # Verificar que el producto existe
    producto = db.query(Producto).filter(Producto.id == movimiento.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Crear el movimiento
    db_movimiento = MovimientoInventario(**movimiento.dict())
    
    # Actualizar el stock del producto
    from sqlalchemy import select
    stock_actual = db.scalar(select(Producto.stock_actual).where(Producto.id == producto.id))
    cantidad = movimiento.cantidad
    
    if movimiento.tipo_movimiento == "entrada":
        nuevo_stock = Decimal(str(stock_actual)) + cantidad
    else:  # tipo_movimiento == "salida"
        if Decimal(str(stock_actual)) < cantidad:
            raise HTTPException(
                status_code=400,
                detail="Stock insuficiente para realizar la salida"
            )
        nuevo_stock = Decimal(str(stock_actual)) - cantidad
    
    # Actualizar el stock en la base de datos
    db.query(Producto).filter(Producto.id == producto.id).update(
        {"stock_actual": nuevo_stock},
        synchronize_session="fetch"
    )
    
    try:
        db.add(db_movimiento)
        db.commit()
        db.refresh(db_movimiento)
        return db_movimiento
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error al registrar el movimiento: {str(e)}"
        )

@router.get("/movimientos/", response_model=List[MovimientoBase])
async def listar_movimientos(
    skip: int = 0,
    limit: int = 100,
    producto_id: Optional[int] = None,
    tipo_movimiento: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MovimientoInventario)
    if producto_id:
        query = query.filter(MovimientoInventario.producto_id == producto_id)
    if tipo_movimiento:
        query = query.filter(MovimientoInventario.tipo_movimiento == tipo_movimiento)
    return query.offset(skip).limit(limit).all()

# Endpoints para Suministros
@router.post("/suministros/", response_model=SuministroBase, status_code=status.HTTP_201_CREATED)
async def crear_suministro(suministro: SuministroCreate, db: Session = Depends(get_db)):
    # Verificar que el producto existe
    producto = db.query(Producto).filter(Producto.id == suministro.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db_suministro = Suministro(**suministro.dict())
    
    try:
        db.add(db_suministro)
        db.commit()
        db.refresh(db_suministro)
        return db_suministro
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear el suministro: {str(e)}"
        )

@router.get("/suministros/", response_model=List[SuministroBase])
async def listar_suministros(
    skip: int = 0,
    limit: int = 100,
    producto_id: Optional[int] = None,
    estado: Optional[EstadoSuministro] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Suministro)
    if producto_id:
        query = query.filter(Suministro.producto_id == producto_id)
    if estado:
        query = query.filter(Suministro.estado == estado)
    return query.offset(skip).limit(limit).all()

@router.get("/suministros/{suministro_id}", response_model=SuministroBase)
async def obtener_suministro(suministro_id: int, db: Session = Depends(get_db)):
    suministro = db.query(Suministro).filter(Suministro.id == suministro_id).first()
    if suministro is None:
        raise HTTPException(status_code=404, detail="Suministro no encontrado")
    return suministro

@router.put("/suministros/{suministro_id}", response_model=SuministroBase)
async def actualizar_suministro(
    suministro_id: int,
    suministro_update: SuministroUpdate,
    db: Session = Depends(get_db)
):
    db_suministro = db.query(Suministro).filter(Suministro.id == suministro_id).first()
    if db_suministro is None:
        raise HTTPException(status_code=404, detail="Suministro no encontrado")
    
    update_data = suministro_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_suministro, field, value)
    
    try:
        db.commit()
        db.refresh(db_suministro)
        return db_suministro
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error al actualizar el suministro: {str(e)}"
        )

@router.delete("/suministros/{suministro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_suministro(suministro_id: int, db: Session = Depends(get_db)):
    suministro = db.query(Suministro).filter(Suministro.id == suministro_id).first()
    if suministro is None:
        raise HTTPException(status_code=404, detail="Suministro no encontrado")
    
    try:
        db.delete(suministro)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error al eliminar el suministro: {str(e)}"
        )
