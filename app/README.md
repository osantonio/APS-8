# Sistema Administrativo APS (Asilo Perpetuo Socorro)

Sistema de gestión administrativa desarrollado para el Asilo Perpetuo Socorro, diseñado para optimizar las operaciones diarias y mejorar el bienestar de los residentes.

## Características Principales

- Gestión de colaboradores y turnos
- Administración de residentes
- Control de inventarios
- Sistema de remisiones
- Seguimiento de actividades

## Requisitos Técnicos

- Python 3.8 o superior
- SQLite3
- Navegador web moderno

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd app
```

2. Crear y activar el entorno virtual:
```bash
# En macOS/Linux
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar la aplicación:
```bash
cd src
uvicorn main:app --reload
```

La aplicación estará disponible en: http://localhost:8000

## Documentación API

- Documentación interactiva: http://localhost:8000/docs
- Documentación alternativa: http://localhost:8000/redoc

## Estructura del Proyecto

```
app/
├── src/
│   ├── models/      # Modelos de la base de datos
│   ├── routes/      # Rutas y endpoints de la API
│   ├── templates/   # Plantillas Jinja2
│   ├── static/      # Archivos estáticos (CSS, JS, imágenes)
│   └── main.py      # Punto de entrada de la aplicación
├── tests/           # Pruebas unitarias y de integración
├── venv/            # Entorno virtual (no versionado)
├── requirements.txt # Dependencias del proyecto
└── README.md        # Este archivo
```

## Desarrollo

Para contribuir al proyecto:

1. Crear una rama para la nueva característica
2. Desarrollar y probar los cambios
3. Crear un pull request con una descripción detallada

## Licencia

Este proyecto es privado y de uso exclusivo para el Asilo Perpetuo Socorro.
