
import csv
import json
from pathlib import Path


# Rutas del proyecto
RAIZ = Path(__file__).resolve().parent.parent

RUTA_CSV = RAIZ / "data/raw/datos_meteorologicos_prueba.csv"
RUTA_JSON = RAIZ / "data/datos.json"


def convertir_dataset(ruta_csv, ruta_json):
    """Convierte el CSV meteorológico al JSON de ClimeGreen."""

    datos = []

    with open(ruta_csv, "r", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            registro = {
                "fecha": fila["fecha"],
                "zona": fila["zona"],
                "temperatura": float(fila["temperatura_media_c"]),
                "humedad": float(fila["humedad_pct"]),
                "viento": float(fila["viento_kmh"]),
                "lluvia": float(fila["precipitacion_mm"])
            }

            datos.append(registro)

    with open(ruta_json, "x", encoding="utf-8") as archivo:
        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False,
            allow_nan=False
        )

    print(f"Registros convertidos: {len(datos)}")
    print(f"JSON generado en: {ruta_json}")


if __name__ == "__main__":
    convertir_dataset(RUTA_CSV, RUTA_JSON)
