#!/usr/bin/env bash

set -euo pipefail

ENV_NAME="venv_leads"
PYTHON_BIN="python3"

echo "🚀 Instalador automático para Debian/Ubuntu"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "📦 python3 no encontrado. Instalando dependencias del sistema..."
  sudo apt-get update
  sudo apt-get install -y python3 python3-venv python3-pip build-essential
fi

if [ ! -d "$ENV_NAME" ]; then
  echo "🧪 Creando entorno virtual: $ENV_NAME"
  "$PYTHON_BIN" -m venv "$ENV_NAME"
else
  echo "ℹ️ El entorno $ENV_NAME ya existe. Se reutilizará."
fi

# shellcheck disable=SC1090
source "$ENV_NAME/bin/activate"

python -m pip install --upgrade pip

if [ -f requirements.txt ]; then
  echo "📦 Instalando dependencias desde requirements.txt"
  pip install -r requirements.txt
else
  echo "📦 requirements.txt no existe, instalando paquete base"
  pip install pandas numpy requests tqdm openpyxl
fi

mkdir -p app scripts data/raw data/processed logs

echo "✅ Instalación terminada"
echo "Siguiente paso:"
echo "  source $ENV_NAME/bin/activate"
echo "  python scripts/run_bi_pipeline.py"
