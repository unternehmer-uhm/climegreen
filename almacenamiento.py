#
import json
import shutil
import tempfile
from pathlib import Path


# Zonas geográficas admitidas por ClimeGreen.
# Zonas geográficas de Madrid admitidas por ClimeGreen.
ZONAS_VALIDAS = [
    "Centro",
    "Norte",
    "Sur",
    "Este",
    "Oeste"
]

#funcion para cargar y leer los datos
def cargar_datos(ruta_json) -> list[dict]:
    """Carga los registros meteorológicos desde un archivo JSON."""
    try:
        with open(ruta_json, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ValueError("El JSON debe contener una lista")

        if not all(isinstance(r, dict) for r in datos):
            raise ValueError("Los registros deben ser diccionarios")

        return datos

    except (OSError, ValueError) as error:
        print(f"Aviso: no se pudieron cargar los datos: {error}")
        return []

#funcion para guarda los datos
def guardar_datos(ruta_json, datos) -> None:
    """Guarda los registros creando una copia de seguridad."""
    ruta = Path(ruta_json)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = None

    try:
        # Crear un archivo temporal con los nuevos datos.
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=ruta.parent,
            delete=False
        ) as archivo:
            temporal = Path(archivo.name)

            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False,
                allow_nan=False
            )

        # Crear una copia de seguridad del archivo original.
        if ruta.exists():
            copia = ruta.with_suffix(ruta.suffix + ".bak")
            shutil.copy2(ruta, copia)

        # Sustituir el archivo original por el nuevo.
        temporal.replace(ruta)

    finally:
        # Eliminar el archivo temporal si todavía existe.
        if temporal is not None:
            temporal.unlink(missing_ok=True)

#funcion para agregar datos nuevos
def agregar_registro(datos, registro) -> bool:
    """Añade un registro si no existe la misma fecha y zona."""

    for existente in datos:
        if (
            existente["fecha"] == registro["fecha"]
            and existente["zona"] == registro["zona"]
        ):
            print("Aviso: ya existe un registro para esa fecha y zona")
            return False

    datos.append(registro)
    return True

#funcion para filtrar zonas
def filtrar_por_zona(datos, zona) -> list[dict]:
    """Devuelve los registros correspondientes a una zona."""
    return [
        registro for registro in datos
        if registro["zona"] == zona
    ]
