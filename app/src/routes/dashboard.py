from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.src.routes.auth import obtener_usuario_actual

router = APIRouter()

# Configurar templates
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/dashboard")
async def mostrar_dashboard(
    request: Request, 
    usuario_actual = Depends(obtener_usuario_actual)
):
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "usuario": usuario_actual,
        "titulo": "Panel Principal"
    })
