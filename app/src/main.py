from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Crear la aplicación FastAPI
app = FastAPI(
    title="APS - Sistema Administrativo",
    description="Sistema de gestión para el Asilo Perpetuo Socorro",
    version="0.8.0"
)

# Configurar archivos estáticos y templates
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Ruta principal
@app.get("/")
async def pagina_principal(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "titulo": "Bienvenido al Sistema APS"}
    )

# Verificación del estado de la API
@app.get("/estado")
async def verificar_estado():
    return {
        "estado": "activo",
        "version": "1.0.0",
        "nombre": "Sistema Administrativo APS"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
