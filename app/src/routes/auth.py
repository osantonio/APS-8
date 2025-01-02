from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.src.models.database import get_db
from app.src.models.colaboradores import Colaborador, RolAcceso
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Configurar templates
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter()

@router.get("/login")
async def mostrar_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def iniciar_sesion(
    request: Request, 
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    try:
        # Buscar colaborador por correo
        colaborador = db.query(Colaborador).filter(Colaborador.correo == form_data.username).first()
        
        if not colaborador or not colaborador.verificar_contrasena(form_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Aquí deberías generar un token de sesión o JWT en un escenario real
        # Por ahora, simularemos la sesión
        response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="usuario_id", value=str(colaborador.id))
        response.set_cookie(key="rol", value=colaborador.rol.value)
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logout")
async def cerrar_sesion():
    response = RedirectResponse(url="/login")
    response.delete_cookie("usuario_id")
    response.delete_cookie("rol")
    return response

# Dependencia para verificar la autenticación
async def obtener_usuario_actual(
    request: Request, 
    db: Session = Depends(get_db)
):
    usuario_id = request.cookies.get("usuario_id")
    if not usuario_id:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    usuario = db.query(Colaborador).filter(Colaborador.id == int(usuario_id)).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    return usuario

# Decorador para verificar roles
def requiere_rol(roles_permitidos=None):
    async def verificar_rol(
        usuario: Colaborador = Depends(obtener_usuario_actual)
    ):
        if roles_permitidos and usuario.rol not in roles_permitidos:
            raise HTTPException(
                status_code=403, 
                detail="No tienes permiso para acceder a este recurso"
            )
        return usuario
    return verificar_rol
