# 🧠 Generador de Leads B2B (DENUE + CompraNet + DataMéxico)

## 📌 Descripción del Proyecto

Este proyecto implementa un **pipeline de datos para prospección comercial B2B**.
El objetivo es identificar y clasificar empresas mexicanas con mayor probabilidad de convertirse en clientes para servicios IT/IA/BI.

---

## 🎯 Objetivo de Negocio

Construir un **directorio de leads accionables y priorizados** con:

- Datos de contacto (teléfono/correo/web)
- Señales de capacidad de pago
- Indicadores de actividad y tamaño empresarial
- Ranking automático para enfoque comercial

---

## 🧩 Fuentes de Datos

1. **DENUE (INEGI)**: universo de empresas, actividad económica, ubicación y contacto.
2. **CompraNet**: evidencia de contratación pública y montos.
3. **DataMéxico**: contexto económico para análisis complementario.

---

## 🏗️ Arquitectura del Flujo

```text
DENUE + CompraNet
      │
      ▼
Normalización de datos
      │
      ▼
Cálculo de métricas BI
      │
      ▼
Score de lead (0-100)
      │
      ▼
Segmentación: Bajo / Medio / Alto / Prioritario
```

---

## 🧮 Métricas BI implementadas

El scoring consolidado (`score_lead`) usa ponderaciones configurables:

- **30%** Contactabilidad (`tiene_telefono`, `tiene_email`, `tiene_web`)
- **20%** Tamaño de empresa (`estrato`)
- **15%** Afinidad sectorial (`actividad_economica`)
- **20%** Historial de contratos públicos (`num_contratos`)
- **15%** Monto acumulado de contratos (`monto_total`)

### Segmentos automáticos

- `0-35`: Bajo
- `35-60`: Medio
- `60-80`: Alto
- `80-100`: Prioritario

---

## ⚙️ Instalación automática (Debian/Ubuntu)

```bash
chmod +x install_leads.sh
./install_leads.sh
```

Este instalador:

- Crea/rehúsa `venv_leads`
- Instala dependencias desde `requirements.txt`
- Deja listas las carpetas `data/raw`, `data/processed`, `logs`

---

## ▶️ Ejecución del pipeline BI

1) Copia tus archivos base:

- `leads_denue_*.csv`
- `leads_compranet_*_contratos.csv` (opcional pero recomendado)

2) Ejecuta:

```bash
source venv_leads/bin/activate
python scripts/run_bi_pipeline.py
```

O con wrapper:

```bash
./denue_extractor.sh
```

---

## 📂 Salidas

En `data/processed/` se generan:

- `leads_scored_YYYYMMDD.csv` → empresas clasificadas con score
- `bi_summary_YYYYMMDD.csv` → KPIs ejecutivos

---

## 📞 Uso Comercial

Con el `leads_scored` puedes:

- Atacar primero el segmento `Prioritario`
- Crear listas para CRM y campañas outbound
- Diseñar dashboards por estado/sector/tamaño

