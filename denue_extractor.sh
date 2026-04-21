#!/usr/bin/env bash

set -euo pipefail

ENV_PATH="venv_leads"
LOG_DIR="logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/pipeline_$TIMESTAMP.log"

echo "🚀 Ejecutando pipeline de BI. Log: $LOG_FILE"

if [ ! -d "$ENV_PATH" ]; then
  echo "❌ Entorno no encontrado: $ENV_PATH"
  echo "Ejecuta primero: ./install_leads.sh"
  exit 1
fi

# shellcheck disable=SC1090
source "$ENV_PATH/bin/activate"

python scripts/run_bi_pipeline.py 2>&1 | tee "$LOG_FILE"
EXIT_CODE=${PIPESTATUS[0]}

deactivate || true

if [ $EXIT_CODE -ne 0 ]; then
  echo "❌ Error en pipeline. Revisa: $LOG_FILE"
  exit $EXIT_CODE
fi

echo "✅ Pipeline finalizado"
