#!/usr/bin/env bash

set -e

ENV_PATH="venv_leads"
SCRIPT="denue_leads_extractor.py"
LOG_DIR="logs"

mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/run_$TIMESTAMP.log"

echo "🚀 Ejecutando con log en $LOG_FILE"

# Validar entorno
if [ ! -d "$ENV_PATH" ]; then
    echo "❌ Entorno no encontrado: $ENV_PATH"
    exit 1
fi

# Validar script
if [ ! -f "$SCRIPT" ]; then
    echo "❌ Script no encontrado: $SCRIPT"
    exit 1
fi

# Activar entorno
source "$ENV_PATH/bin/activate"

# Ejecutar script con log (stdout + stderr)
python "$SCRIPT" 2>&1 | tee "$LOG_FILE"

# Guardar exit code real del script Python
EXIT_CODE=${PIPESTATUS[0]}

# Desactivar entorno
deactivate

# Validar ejecución
if [ $EXIT_CODE -ne 0 ]; then
    echo "❌ Error en ejecución. Revisa log: $LOG_FILE"
    exit $EXIT_CODE
fi

echo "✅ Proceso terminado correctamente"