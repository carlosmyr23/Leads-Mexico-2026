# 🧠 Generador de Leads B2B (DENUE + CompraNet + DataMéxico)

## 📌 Descripción del Proyecto

Este proyecto implementa un **pipeline de datos enfocado en prospección comercial B2B**, cuyo objetivo es identificar **empresas clave en México junto con sus datos de contacto (teléfono y correo)** para ofrecer servicios de tecnología (IT, IA, BI, automatización).

A diferencia de un simple ETL, este sistema está diseñado como un **motor de generación de leads**, priorizando empresas con:

- Actividad económica activa
- Capacidad de pago
- Participación en contratos públicos
- Presencia verificable (contacto disponible)

---

## 🎯 Objetivo de Negocio

Construir un **directorio de leads accionables** para ventas de servicios IT, enfocado en:

- Empresas con **teléfono y/o correo disponible**
- Empresas con **capacidad de compra real**
- Empresas que ya consumen servicios (ej. gobierno → CompraNet)

El output final permite:

- Prospección directa (llamadas / correo)
- Alimentar CRM
- Automatizar outreach con bots
- Priorizar leads con mayor probabilidad de conversión

---

## 🧩 Fuentes de Datos

### 1. DENUE (INEGI)
Fuente principal para identificación de empresas.

Incluye:
- Nombre de empresa
- Actividad económica
- Dirección
- Teléfono (cuando está disponible)
- Tamaño de empresa
- Estatus operativo

👉 **Rol en el sistema:**  
Base de universo de empresas + primer punto de contacto

---

### 2. CompraNet
Fuente para identificar empresas con capacidad económica.

Incluye:
- Proveedores del gobierno
- Montos de contratos
- Dependencias
- Historial de compras

👉 **Rol en el sistema:**  
Filtro de empresas con **capacidad de pago comprobada**

---

### 3. DataMéxico
Fuente contextual.

Incluye:
- Indicadores económicos
- Datos por industria
- Tendencias

👉 **Rol en el sistema:**  
Enriquecimiento para análisis y segmentación

---

## 🧠 Lógica de Generación de Leads

El sistema sigue esta lógica:

1. Obtener empresas desde DENUE  
2. Filtrar empresas activas  
3. Identificar empresas con teléfono disponible  
4. Cruzar con CompraNet para detectar:
   - Proveedores del gobierno
   - Empresas con contratos relevantes  
5. Generar dataset final de leads priorizados  

---

## 🏗️ Arquitectura del Pipeline

DENUE (empresas + contacto)
│
▼
Filtrado (empresas activas)
│
▼
Enriquecimiento (CompraNet)
│
▼
Priorización (capacidad económica)
│
▼
Dataset de leads accionables


---

## ⚙️ Pipeline

El flujo técnico realiza:

- Extracción desde APIs públicas
- Descarga de datasets masivos (CompraNet)
- Normalización de datos
- Integración entre fuentes
- Exportación a CSV listo para uso comercial

---

## 🛠️ Componentes Principales

### 🔹 `extract_denue()`
Extrae empresas desde DENUE con:

- Paginación
- Filtrado por entidad
- Obtención de datos de contacto

---

### 🔹 `extract_compranet()`
Descarga y unifica:

- Contratos
- Expedientes

Permite identificar empresas con historial de compra pública.

---

### 🔹 `datamx_get()`
Consulta indicadores económicos para:

- Enriquecer análisis
- Apoyar segmentación futura

---

### 🔹 `run_pipeline()`
Orquesta todo el flujo:

- Ejecuta extracciones
- Consolida datos
- Genera datasets finales

---

## 📂 Outputs

El sistema genera archivos CSV listos para prospección:

- `denue_YYYYMMDD.csv`
- `compranet_YYYYMMDD.csv`
- `datamexico_YYYYMMDD.csv`

---

## 📞 Uso Comercial del Output

Los datos generados pueden usarse para:

### 🔹 Prospección directa
- Llamadas a empresas (teléfono)
- Envío de correos

### 🔹 Automatización
- Bots de contacto (WhatsApp / email)
- Secuencias automatizadas de ventas

### 🔹 CRM
- Carga en HubSpot, Salesforce, etc.
- Seguimiento de leads

---

## 🧮 Estrategia de Priorización (Leads)

Ejemplo de scoring futuro:

| Variable | Peso |
|--------|------|
| Tiene teléfono | Alto |
| Participa en CompraNet | Alto |
| Monto contratado | Muy alto |
| Tamaño de empresa | Medio |
| Sector | Variable |

---

## 🧹 Limpieza de Datos

Se normalizan columnas:

```python
df.columns = df.columns.str.lower()
