# CLIMEGREEN — Sistema de Monitorización Climática Urbana

![Estado](https://img.shields.io/badge/estado-MVP-yellow) ![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![Tests](https://img.shields.io/badge/tests-pytest-green)

Aplicación de terminal (MVP) desarrollada para el **Departamento de Resiliencia Urbana y Smart City** del Ayuntamiento. Permite a los técnicos de distrito digitalizar las mediciones meteorológicas manuales de parques históricos y huertos urbanos, validar la calidad de los datos, almacenarlos de forma persistente en JSON sin pérdida de información y activar alertas tempranas para los departamentos de Obras y Movilidad.

---

## Características principales

| # | Característica | Descripción |
|:-:|---|---|
| 1 | **Registro guiado y validado** | Captura de fecha (`AAAA-MM-DD`), zona geográfica, temperatura (°C), humedad (%), viento (km/h) y lluvia (mm) con control de tipos, rangos lógicos y reintentos automáticos ante entradas erróneas. |
| 2 | **Prevención de duplicados** | Detecta si ya existe una medición para la misma fecha y zona, solicitando confirmación explícita antes de sobrescribir. |
| 3 | **Persistencia segura en JSON** | Lee el histórico inicial (`data/clima_historico.json`) y añade nuevos registros sin borrar los anteriores. |
| 4 | **Alertas tempranas** | Evalúa automáticamente umbrales de riesgo (amarillo y rojo) por calor, viento y lluvia. |
| 5 | **Consulta y estadísticas por zona** | Filtra registros por distrito o zona y calcula métricas básicas (temperatura media/máxima, humedad media, viento máximo y lluvia acumulada). |
| 6 | **Trazabilidad mediante logs** | Registra las operaciones y alertas activadas en `logs/climegreen.log`. |
| 7 | **Pruebas unitarias** | Batería de tests automáticos con pytest para verificar validaciones, alertas y persistencia. |

---

## Estructura del proyecto

```text
climegreen/
├── data/
│   └── clima_historico.json   # Dataset inicial (mock) e histórico persistente
├── logs/
│   └── climegreen.log         # Registro de eventos (generado al ejecutar)
├── tests/
│   └── test_app.py            # Pruebas unitarias con pytest
├── alertas.py                 # Lógica de alertas meteorológicas y estadísticas
├── almacenamiento.py          # Lectura/escritura JSON, filtrado y duplicados
├── main.py                    # Punto de entrada y menú interactivo de consola
├── validaciones.py            # Validación de fechas, textos y rangos numéricos
├── .gitignore                 # Exclusiones de Git (venv, cache, logs)
├── requirements.txt           # Dependencias externas del proyecto
└── README.md                  # Documentación del proyecto
```

---

## Requisitos e instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd climegreen
```

### 2. Crear y activar el entorno virtual

**Linux / WSL / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Uso de la aplicación

Ejecuta el programa principal desde la raíz del proyecto con el entorno virtual activado:

```bash
python3 main.py
```

### Opciones del menú principal

| Opción | Descripción |
|:------:|---|
| **1** — Registrar medición | Solicita fecha, zona, temperatura (°C), humedad (%), viento (km/h) y lluvia (mm). Si algún dato es inválido, muestra el error y vuelve a pedirlo. Al guardar, informa si se ha activado alguna alerta. |
| **2** — Consultar por zona | Busca mediciones por nombre de zona o distrito (o deja el campo vacío para listar todo el histórico) y muestra un resumen estadístico de los registros filtrados. |
| **3** — Salir | Cierra la aplicación de forma segura. |

---

## Ejemplo de flujo en consola

```text
==========================================
  CLIMEGREEN - RESILIENCIA URBANA
==========================================
1. Registrar medición
2. Consultar por zona
3. Salir
Elige una opción (1-3): 1

--- REGISTRAR MEDICIÓN MANUAL ---
Fecha (AAAA-MM-DD): 2026-11-25
Zona (ej. Parque del Retiro): Parque del Retiro
Temperatura (°C): 41.2
Humedad (%): 115
  [Error] Humedad fuera de rango (0.0 a 100.0). Recibido: 115.0. Inténtalo de nuevo.
Humedad (%): 35
Viento (km/h): 18
Lluvia (mm): 0

Registro guardado correctamente.

*** PROTOCOLOS DE ALERTA ACTIVADOS ***
  - ALERTA ROJA CALOR: Temperatura extrema (41.2 °C >= 40 °C).
```

---

## Reglas de validación y umbrales de alerta

### Rangos válidos de entrada

| Campo | Formato / Rango |
|---|---|
| Fecha | `AAAA-MM-DD` (fecha válida de calendario) |
| Temperatura | −25.0 a 55.0 °C |
| Humedad | 0.0 a 100.0 % |
| Viento | 0.0 a 200.0 km/h |
| Lluvia | 0.0 a 500.0 mm |

### Umbrales de activación de alertas

| Fenómeno | Alerta amarilla | Alerta roja |
|---|:---:|:---:|
| Calor | ≥ 35.0 °C | ≥ 40.0 °C |
| Viento | ≥ 50.0 km/h | ≥ 70.0 km/h |
| Lluvia | ≥ 15.0 mm | ≥ 30.0 mm |

---

## Pruebas unitarias

Para ejecutar la batería de tests automáticos con pytest:

```bash
pytest -v
```

---

## Equipo y reparto de módulos

| Persona | Módulo | Responsabilidad |
|:---:|---|---|
| 1 | `validaciones.py` | Validación de fechas, textos y rangos numéricos |
| 2 | `almacenamiento.py` + `data/` | Persistencia JSON, filtrado y control de duplicados |
| 3 | `alertas.py` + `logs/` | Umbrales de alerta y registro de eventos |
| 4 | `main.py` + `tests/` | Menú interactivo, integración y pruebas |

---

## Dataset meteorológico y almacenamiento

### Características del dataset

El proyecto incorpora un dataset meteorológico de prueba
correspondiente a Madrid durante el año 2025.

- Archivo CSV: `data/raw/datos_meteorologicos_prueba.csv`.
- Archivo JSON: `data/datos.json`.
- Periodo: del 01/01/2025 al 31/12/2025.
- Total de registros: 1.825.
- Frecuencia: diaria.
- Registros por zona: 365.
- Zonas válidas: Centro, Norte, Sur, Este y Oeste.

Los datos por zona son simulados a partir del dataset inicial
de Madrid con fines educativos. No representan mediciones
meteorológicas oficiales de cada zona.

### Estructura de los registros

| Campo | Descripción | Unidad |
|---|---|---|
| `fecha` | Fecha de la medición | AAAA-MM-DD |
| `zona` | Zona geográfica | Texto |
| `temperatura` | Temperatura media diaria | °C |
| `humedad` | Humedad relativa | % |
| `viento` | Velocidad del viento | km/h |
| `lluvia` | Precipitación diaria | mm |

### Conversión del dataset

El script `scripts/convertir_dataset.py` permite transformar
el archivo CSV al formato JSON utilizado por la aplicación.

Para generar el JSON inicial:

```bash
python scripts/convertir_dataset.py
```

El conversor evita sobrescribir un histórico existente.

### Módulo de almacenamiento

El módulo `almacenamiento.py` proporciona las siguientes
funciones:

| Función | Responsabilidad |
|---|---|
| `cargar_datos()` | Lectura del JSON y gestión de errores. |
| `guardar_datos()` | Escritura segura y copia de seguridad. |
| `agregar_registro()` | Incorporación de registros y rechazo de duplicados. |
| `filtrar_por_zona()` | Consulta de registros por zona geográfica. |

Cada registro se identifica mediante la combinación de fecha
y zona, permitiendo almacenar mediciones de distintas zonas
en un mismo día.

### Pruebas del módulo de almacenamiento

El archivo `tests/test_almacenamiento.py` contiene ocho
pruebas unitarias que verifican la lectura, escritura,
persistencia, gestión de errores, copias de seguridad,
prevención de duplicados y filtrado por zonas.

Para ejecutar las pruebas:

```bash
python -m pytest tests/test_almacenamiento.py -v
```

Las pruebas utilizan archivos temporales para evitar
modificar el histórico meteorológico.
