from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path
from contextlib import asynccontextmanager
from .routes import inventario, remisiones, auth, dashboard
from .models.database import create_tables, engine_async as engine, Base
from .routes.auth import obtener_usuario_actual
import asyncio

# Contexto de ciclo de vida de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializar base de datos al inicio
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cualquier limpieza necesaria al apagar la aplicación puede ir aquí

# Crear la aplicación FastAPI
app = FastAPI(
    title="APS - Sistema Administrativo",
    description="Sistema de gestión para el Asilo Perpetuo Socorro",
    version="0.8.0",
    lifespan=lifespan
)

# Configurar archivos estáticos y templates
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Ruta principal
@app.get("/")
async def pagina_principal(
    request: Request
):
    try:
        usuario = await obtener_usuario_actual(request)
        # Si el usuario está autenticado, redirigir al dashboard
        return RedirectResponse(url="/dashboard")
    except Exception:
        # Si no hay usuario autenticado, mostrar página principal
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "titulo": "Bienvenido al Sistema APS"}
        )

# Ruta de login
@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "titulo": "Iniciar Sesión"}
    )

# Verificación del estado de la API
@app.get("/estado")
async def verificar_estado():
    return {
        "estado": "activo",
        "version": "1.0.0",
        "nombre": "Sistema Administrativo APS"
    }

# Incluir las rutas de inventario, remisiones, autenticación y dashboard
app.include_router(inventario.router)
app.include_router(remisiones.router)
app.include_router(auth.router, prefix="/auth", tags=["autenticación"])
app.include_router(dashboard.router, tags=["dashboard"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
