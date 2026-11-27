
import json

from almacenamiento import (
    cargar_datos,
    guardar_datos,
    agregar_registro,
    filtrar_por_zona
)


# Registros meteorológicos ficticios para las pruebas.
REGISTRO_CENTRO = {
    "fecha": "2025-01-01",
    "zona": "Centro",
    "temperatura": 15.0,
    "humedad": 65.0,
    "viento": 12.0,
    "lluvia": 0.0
}

REGISTRO_NORTE = {
    "fecha": "2025-01-01",
    "zona": "Norte",
    "temperatura": 12.0,
    "humedad": 70.0,
    "viento": 18.0,
    "lluvia": 2.0
}


def test_cargar_datos(tmp_path):
    """Comprueba la lectura de un JSON válido."""
    ruta = tmp_path / "datos.json"

    ruta.write_text(
        json.dumps([REGISTRO_CENTRO]),
        encoding="utf-8"
    )

    datos = cargar_datos(ruta)

    assert datos == [REGISTRO_CENTRO]


def test_cargar_archivo_inexistente(tmp_path):
    """Comprueba que un archivo inexistente devuelve una lista vacía."""
    ruta = tmp_path / "inexistente.json"

    assert cargar_datos(ruta) == []


def test_cargar_json_corrupto(tmp_path):
    """Comprueba que un JSON corrupto no interrumpe la aplicación."""
    ruta = tmp_path / "datos.json"
    ruta.write_text("JSON incorrecto", encoding="utf-8")

    assert cargar_datos(ruta) == []


def test_guardar_sin_borrar_registros(tmp_path):
    """Comprueba que se conservan los registros anteriores."""
    ruta = tmp_path / "datos.json"

    guardar_datos(ruta, [REGISTRO_CENTRO])

    datos = cargar_datos(ruta)
    agregar_registro(datos, REGISTRO_NORTE)
    guardar_datos(ruta, datos)

    assert cargar_datos(ruta) == [
        REGISTRO_CENTRO,
        REGISTRO_NORTE
    ]


def test_copia_seguridad(tmp_path):
    """Comprueba que se conserva la versión anterior del JSON."""
    ruta = tmp_path / "datos.json"

    guardar_datos(ruta, [REGISTRO_CENTRO])

    guardar_datos(
        ruta,
        [REGISTRO_CENTRO, REGISTRO_NORTE]
    )

    copia = tmp_path / "datos.json.bak"

    assert copia.exists()
    assert cargar_datos(copia) == [REGISTRO_CENTRO]


def test_rechazar_duplicado():
    """Comprueba el rechazo de una fecha y zona repetidas."""
    datos = [REGISTRO_CENTRO.copy()]

    duplicado = REGISTRO_CENTRO.copy()
    duplicado["temperatura"] = 20.0

    assert agregar_registro(datos, duplicado) is False
    assert datos == [REGISTRO_CENTRO]


def test_misma_fecha_distinta_zona():
    """Permite registrar diferentes zonas en un mismo día."""
    datos = [REGISTRO_CENTRO.copy()]

    assert agregar_registro(datos, REGISTRO_NORTE.copy()) is True
    assert len(datos) == 2


def test_filtrar_por_zona():
    """Comprueba el filtrado sin modificar la lista original."""
    datos = [REGISTRO_CENTRO, REGISTRO_NORTE]

    assert filtrar_por_zona(datos, "Centro") == [REGISTRO_CENTRO]
    assert filtrar_por_zona(datos, "Norte") == [REGISTRO_NORTE]
    assert filtrar_por_zona(datos, "Sur") == []
    assert len(datos) == 2
