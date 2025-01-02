Hoja de Ruta: Desarrollo de Aplicación Administrativa para el Asilo Perpetuo Socorro

Ocupo de tu ayuda para hacer un proyecto ambicioso como proposito de año nuevo, con mi modesto conocimiento de programacion, el uso de python, sqlite3, y mi macosx en visual studio code, quiero desarrollar una aplicacion que supla todas las necesidades administrativas del centro de vida y bienestar asilo perpetuo socorro, llevar dentro de ella todas las operaciones necesarias para el funcionamiento del centro de vida y para fortalecer el bienestar de los beneficiarios.


Resumen Ejecutivo
El Asilo Perpetuo Socorro busca desarrollar una aplicación web para mejorar la administración y el bienestar de sus residentes. Esta plataforma permitirá la gestión eficiente de colaboradores, residentes, inventarios y actividades, optimizando el tiempo y recursos del personal del asilo.

Objetivo del Proyecto
Desarrollar una plataforma administrativa robusta que permita:

Gestionar horarios y turnos de trabajo de los colaboradores.

Registrar y administrar la información de los residentes.

Monitorear y gestionar el inventario de suministros.

Facilitar la comunicación y seguimiento de remisiones entre colaboradores y profesionales.

Objetivo
Desarrollar una aplicación web que gestione todas las operaciones administrativas del Asilo Perpetuo Socorro, mejorando la eficiencia y el bienestar de sus beneficiarios. La aplicación incluirá funcionalidades para la gestión de colaboradores, residentes, inventarios y actividades.

Tecnologías
Backend: Python, FastAPI

Base de Datos: SQLite

Frontend: Jinja2 templates (fase inicial), Vue.js(fase avanzada)

Servidor: Uvicorn

Fases del Proyecto
Fase 1: Configuración Inicial
Entorno de Desarrollo:

Crear un entorno virtual en Python.

Instalar dependencias necesarias: FastAPI, Uvicorn, SQLite.

Estructura del Proyecto:

Configurar estructura básica del proyecto con un repositorio en GitHub.

Crear el archivo principal de la aplicación.

Fase 2: Gestión de Colaboradores
Modelos de Base de Datos:

Crear modelos para usuarios y roles.

Definir esquema de base de datos para colaboradores.

Autenticación y Autorización:

Implementar registro y login de colaboradores.

Definir permisos y roles (administrador, colaborador).

API de Gestión de Colaboradores:

Crear endpoints para el registro, actualización y eliminación de colaboradores (solo para administradores).

Implementar cambio de turno y horarios de trabajo.

Fase 3: Gestión de Residentes
Modelos de Base de Datos:

Crear modelos para residentes y su información personal.

API de Gestión de Residentes:

Crear endpoints para registrar, actualizar y gestionar residentes.

Implementar cronograma de actividades de los beneficiarios.

Fase 4: Gestión de Inventarios
Modelos de Base de Datos:

Crear modelos para inventario y suministros.

API de Gestión de Inventarios:

Crear endpoints para agregar, actualizar y eliminar suministros.

Implementar sistema de facturación de suministros a los residentes.

Fase 5: Gestión de Remisiones
Modelos de Base de Datos:

Crear modelos para remisiones y seguimientos.

API de Gestión de Remisiones:

Crear endpoints para la creación y seguimiento de remisiones.

Implementar trazabilidad de remisiones por profesionales.

Fase 6: Interfaz de Usuario
Templates con Jinja2:

Diseñar templates iniciales para la interfaz gráfica.

Integrar templates con el backend.

Desarrollo con Vue.js:

Migrar la interfaz gráfica a Vue.js.

Implementar funcionalidad dinámica en el frontend.

Fase 7: Pruebas y Despliegue
Pruebas:

Realizar pruebas unitarias y de integración.

Realizar pruebas de usabilidad con usuarios reales.

Despliegue:

Configurar el servidor para el despliegue de la aplicación.

Realizar el despliegue en un servidor de producción.

Dependencias Principales
FastAPI: Framework para el desarrollo de APIs.

Uvicorn: Servidor ASGI para correr la aplicación FastAPI.

SQLite: Base de datos ligera y fácil de usar.

Jinja2: Motor de templates para la fase inicial del frontend.

Vue.js: Framework para la construcción de interfaces de usuario dinámicas en la fase avanzada.