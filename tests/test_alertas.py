"""Pruebas unitarias para el módulo alertas.py."""

import pytest

from alertas import evaluar_alertas, evaluar_registro, formatear_bloque_alertas


def test_sin_alertas_en_condiciones_normales() -> None:
    """Devuelve lista vacía cuando ninguna variable supera el umbral inferior."""
    resultado = evaluar_alertas(temperatura=24.0, viento=18.5, lluvia=0.0)
    assert resultado == []


def test_umbrales_exactos_activan_alertas_correspondientes() -> None:
    """Los valores iguales al umbral (>=) deben activar la alerta."""
    assert evaluar_alertas(35.0, 0.0, 0.0) == [
        "ALERTA AMARILLA POR CALOR (35.0 °C >= 35 °C)"
    ]
    assert evaluar_alertas(40.0, 0.0, 0.0) == [
        "ALERTA ROJA POR CALOR EXTREMO (40.0 °C >= 40 °C)"
    ]
    assert evaluar_alertas(0.0, 50.0, 0.0) == [
        "ALERTA NARANJA POR VIENTO (50.0 km/h >= 50 km/h)"
    ]
    assert evaluar_alertas(0.0, 70.0, 0.0) == [
        "ALERTA ROJA POR VIENTO FUERTE (70.0 km/h >= 70 km/h)"
    ]
    assert evaluar_alertas(0.0, 0.0, 15.0) == [
        "ALERTA AMARILLA POR LLUVIA INTENSA (15.0 mm >= 15 mm)"
    ]
    assert evaluar_alertas(0.0, 0.0, 40.0) == [
        "ALERTA ROJA POR LLUVIA TORRENCIAL (40.0 mm >= 40 mm)"
    ]


def test_nivel_rojo_excluye_nivel_inferior_de_la_misma_variable() -> None:
    """Si se supera el umbral rojo, no debe añadirse también el umbral menor."""
    resultado = evaluar_alertas(temperatura=42.5, viento=75.0, lluvia=45.0)
    assert len(resultado) == 3
    assert resultado[0] == "ALERTA ROJA POR CALOR EXTREMO (42.5 °C >= 40 °C)"
    assert resultado[1] == "ALERTA ROJA POR VIENTO FUERTE (75.0 km/h >= 70 km/h)"
    assert resultado[2] == "ALERTA ROJA POR LLUVIA TORRENCIAL (45.0 mm >= 40 mm)"


def test_alertas_simultaneas_en_varias_variables() -> None:
    """Permite acumular alertas de distintas variables en una misma lectura."""
    resultado = evaluar_alertas(temperatura=36.0, viento=55.0, lluvia=20.0)
    assert resultado == [
        "ALERTA AMARILLA POR CALOR (36.0 °C >= 35 °C)",
        "ALERTA NARANJA POR VIENTO (55.0 km/h >= 50 km/h)",
        "ALERTA AMARILLA POR LLUVIA INTENSA (20.0 mm >= 15 mm)",
    ]


@pytest.mark.parametrize(
    ("registro", "esperado"),
    [
        (
            {
                "fecha": "2026-07-15",
                "zona": "Parque del Retiro",
                "temperatura": 41.2,
                "humedad": 25.0,
                "viento": 52.0,
                "lluvia": 0.0,
            },
            [
                "ALERTA ROJA POR CALOR EXTREMO (41.2 °C >= 40 °C)",
                "ALERTA NARANJA POR VIENTO (52.0 km/h >= 50 km/h)",
            ],
        ),
        (
            {
                "fecha": "2026-11-28",
                "zona": "Huertos Urbanos Norte",
                "temperatura": "14.5",
                "viento": "12",
                "lluvia": "0",
            },
            [],
        ),
    ],
)
def test_evaluar_registro_con_diccionario(
    registro: dict, esperado: list[str]
) -> None:
    """Comprueba evaluar_registro con distintos tipos numéricos en el diccionario."""
    assert evaluar_registro(registro) == esperado


def test_formatear_bloque_alertas_con_y_sin_alertas() -> None:
    """Verifica el mensaje formateado para consola cuando hay o no alertas."""
    assert formatear_bloque_alertas([], zona="Centro") == (
        "Sin alertas meteorológicas activadas."
    )

    salida = formatear_bloque_alertas(
        ["ALERTA NARANJA POR VIENTO (55.0 km/h >= 50 km/h)"],
        zona="Centro",
    )
    assert "Protocolos activados en Centro:" in salida
    assert "ALERTA NARANJA POR VIENTO (55.0 km/h >= 50 km/h)" in salida
