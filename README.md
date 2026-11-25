CLIMEGREEN - SISTEMA DE MONITORIZACION CLIMATICA URBANA
========================================================

Aplicacion de terminal (MVP) desarrollada para el Departamento de Resiliencia Urbana y Smart City del Ayuntamiento. Permite a los tecnicos de distrito digitalizar las mediciones meteorologicas manuales de parques historicos y huertos urbanos, validar la calidad de los datos, almacenarlos de forma persistente en JSON sin perdida de informacion y activar alertas tempranas para los departamentos de Obras y Movilidad.


CARACTERISTICAS PRINCIPALES
---------------------------
- Registro guiado y validado: Captura de fecha (AAAA-MM-DD), zona geografica, temperatura (C), humedad (%), viento (km/h) y lluvia (mm) con control de tipos, rangos logicos y reintentos automaticos ante entradas erroneas.
- Prevencion de duplicados: Detecta si ya existe una medicion para la misma fecha y zona, solicitando confirmacion explicita antes de sobrescribir.
- Persistencia segura en JSON: Lee el historico inicial (data/clima_historico.json) y anade nuevos registros sin borrar los anteriores.
- Sistema de alertas tempranas: Evalua automaticamente umbrales de riesgo (amarillo y rojo) por calor, viento y lluvia.
- Consulta y estadisticas por zona: Filtra registros por distrito o zona y calcula metricas basicas (temperatura media/maxima, humedad media, viento maximo y lluvia acumulada).
- Trazabilidad mediante logs: Registra las operaciones y alertas activadas en logs/climegreen.log.
- Pruebas unitarias: Bateria de tests automaticos con pytest para verificar validaciones, alertas y persistencia.


ESTRUCTURA DEL PROYECTO
-----------------------
climegreen/
  data/
    clima_historico.json   -> Dataset inicial (mock) e historico persistente
  logs/
    climegreen.log        -> Archivo de registro de eventos (generado al ejecutar)
  tests/
    test_app.py            -> Pruebas unitarias con pytest
  alertas.py               -> Logica de alertas meteorologicas y estadisticas
  almacenamiento.py        -> Lectura/escritura JSON, filtrado y control de duplicados
  main.py                  -> Punto de entrada y menu interactivo de consola
  validaciones.py          -> Validacion de fechas, textos y rangos numericos
  .gitignore               -> Exclusiones de Git (venv, cache, logs)
  requirements.txt         -> Dependencias externas del proyecto
  README.md                -> Documentacion del proyecto


REQUISITOS E INSTALACION
------------------------
1. Clonar el repositorio y entrar en la carpeta:
   git clone <URL_DEL_REPOSITORIO>
   cd climegreen

2. Crear y activar el entorno virtual (venv):
   En Linux / WSL / macOS:
     python3 -m venv venv
     source venv/bin/activate

   En Windows (PowerShell):
     python -m venv venv
     .\venv\Scripts\Activate.ps1

3. Instalar dependencias:
   pip install -r requirements.txt


USO DE LA APLICACION
--------------------
Ejecuta el programa principal desde la raiz del proyecto con el entorno virtual activado:
   python3 main.py

Opciones del menu principal:
1. Registrar medicion: Solicita fecha, zona, temperatura (C), humedad (%), viento (km/h) y lluvia (mm). Si algun dato es invalido, muestra el error y vuelve a pedirlo. Al guardar, informa si se ha activado alguna alerta.
2. Consultar por zona: Permite buscar mediciones por nombre de zona o distrito (o dejar el campo vacio para listar todo el historico) y muestra un resumen estadistico de los registros filtrados.
3. Salir: Cierra la aplicacion de forma segura.


EJEMPLO DE FLUJO EN CONSOLA
---------------------------
==========================================
  CLIMEGREEN - RESILIENCIA URBANA
==========================================
1. Registrar medicion
2. Consultar por zona
3. Salir
Elige una opcion (1-3): 1

--- REGISTRAR MEDICION MANUAL ---
Fecha (AAAA-MM-DD): 2026-11-25
Zona (ej. Parque del Retiro): Parque del Retiro
Temperatura (C): 41.2
Humedad (%): 115
  [Error] Humedad fuera de rango (0.0 a 100.0). Recibido: 115.0. Intentalo de nuevo.
Humedad (%): 35
Viento (km/h): 18
Lluvia (mm): 0

Registro guardado correctamente.

*** PROTOCOLOS DE ALERTA ACTIVADOS ***
  - ALERTA ROJA CALOR: Temperatura extrema (41.2 C >= 40 C).


REGLAS DE VALIDACION Y UMBRALES DE ALERTA
-----------------------------------------
Rangos validos de entrada:
- Fecha: formato AAAA-MM-DD (fecha valida de calendario)
- Temperatura: -25.0 a 55.0 C
- Humedad: 0.0 a 100.0 %
- Viento: 0.0 a 200.0 km/h
- Lluvia: 0.0 a 500.0 mm

Umbrales de activacion de alertas:
- Calor:
    Alerta Amarilla: >= 35.0 C
    Alerta Roja:     >= 40.0 C
- Viento:
    Alerta Amarilla: >= 50.0 km/h
    Alerta Roja:     >= 70.0 km/h
- Lluvia:
    Alerta Amarilla: >= 15.0 mm
    Alerta Roja:     >= 30.0 mm


PRUEBAS UNITARIAS
-----------------
Para ejecutar la bateria de tests automaticos con pytest:
   pytest -v
