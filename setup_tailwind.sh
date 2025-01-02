#!/bin/bash

# Instalar Node.js si no está instalado
if ! command -v node &> /dev/null
then
    echo "Node.js no está instalado. Por favor, instálalo primero."
    exit 1
fi

# Instalar dependencias de Node.js
npm install

# Instalar Tailwind CSS y Daisy UI globalmente
npm install -g tailwindcss postcss autoprefixer daisyui

# Compilar Tailwind CSS
npx tailwindcss -i ./app/src/static/css/input.css -o ./app/src/static/css/output.css

# Verificar si la compilación fue exitosa
if [ -f "./app/src/static/css/output.css" ]; then
    echo "Compilación de Tailwind CSS exitosa"
else
    echo "Error en la compilación de Tailwind CSS"
    exit 1
fi
