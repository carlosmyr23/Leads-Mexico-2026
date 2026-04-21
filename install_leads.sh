#!/usr/bin/env bash

set -e  # detener si algo falla

echo "🚀 Creando entorno virtual..."

# Nombre del entorno
ENV_NAME="venv_leads"

# Crear entorno
python3 -m venv $ENV_NAME

echo "✅ Entorno creado: $ENV_NAME"

# Activar entorno
echo "⚙️ Activando entorno..."
source $ENV_NAME/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install requests pandas tqdm

echo "📝 Generando requirements.txt..."
pip freeze > requirements.txt

echo "📁 Creando estructura base..."
mkdir -p app data logs

# Crear archivo base de script
cat <<EOL > app/main.py
import requests
import pandas as pd
import time
import json
import os
from datetime import datetime
from tqdm import tqdm

print("✅ Entorno listo para trabajar")
EOL

echo "🙈 Configurando .gitignore..."
echo -e "venv/\n__pycache__/\n*.pyc\n.env\nlogs/" > .gitignore

echo ""
echo "🎯 SETUP COMPLETO"
echo "Activa el entorno con:"
echo "source $ENV_NAME/bin/activate"