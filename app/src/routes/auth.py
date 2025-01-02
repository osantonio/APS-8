import logging
import traceback
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.src.models.database import get_db
from app.src.models.colaboradores import Colaborador, RolAcceso
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        logger.info(f"Intento de inicio de sesión para: {form_data.username}")
        
        # Buscar colaborador por correo
        colaborador = db.query(Colaborador).filter(Colaborador.correo == form_data.username).first()
        
        if not colaborador:
            logger.warning(f"Usuario no encontrado: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar contraseña con manejo de errores detallado
        logger.info(f"Verificando contraseña para: {form_data.username}")
        
        try:
            # Verificación de contraseña con más información de depuración
            if not colaborador.verificar_contrasena(form_data.password):
                logger.warning(f"Contraseña incorrecta para: {form_data.username}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except ValueError as ve:
            # Manejar específicamente errores de formato de contraseña
            logger.error(f"Error de formato de contraseña: {str(ve)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de contraseña inválido"
            )
        except Exception as e:
            logger.error(f"Error al verificar contraseña: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno al verificar credenciales: {str(e)}"
            )
        
        # Simular la sesión
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="usuario_id", value=str(colaborador.id))
        response.set_cookie(key="rol", value=colaborador.rol.value)
        
        logger.info(f"Inicio de sesión exitoso para: {form_data.username}")
        return response
    
    except HTTPException:
        # Re-raise HTTPException para mantener los detalles originales
        raise
    except Exception as e:
        logger.error(f"Error inesperado en inicio de sesión: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error interno del servidor: {str(e)}"
        )

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
