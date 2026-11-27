"""Módulo de validaciones: nada inválido entra al sistema."""

import math
from datetime import date, datetime

TEMP_MIN, TEMP_MAX = -20, 50       # °C
HUMEDAD_MIN, HUMEDAD_MAX = 0, 100  # %
VIENTO_MIN, VIENTO_MAX = 0, 150    # km/h


def _en_rango(valor, minimo, maximo) -> bool:
    """True si 'valor' es un número real entre minimo y maximo (incluidos)."""
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return False  # letras, None, campo vacío...
    if not math.isfinite(numero):  # rechaza nan e inf
        return False
    return minimo <= numero <= maximo


def validar_fecha(fecha: str) -> bool:
    """Formato DD/MM/YYYY, fecha real y no futura."""
    if not isinstance(fecha, str) or len(fecha.strip()) != 10:
        return False
    try:
        dia = datetime.strptime(fecha.strip(), "%d/%m/%Y").date()
    except ValueError:  # formato malo o fecha inexistente (31/02/2026)
        return False
    return dia <= date.today()


def validar_temperatura(temp: float) -> bool:
    """Rango -20 a 50 °C."""
    return _en_rango(temp, TEMP_MIN, TEMP_MAX)


def validar_humedad(hum: float) -> bool:
    """Rango 0-100 %."""
    return _en_rango(hum, HUMEDAD_MIN, HUMEDAD_MAX)


def validar_viento(viento: float) -> bool:
    """Rango 0-150 km/h."""
    return _en_rango(viento, VIENTO_MIN, VIENTO_MAX)


def validar_lluvia(lluvia: float) -> bool:
    """Lluvia >= 0 mm."""
    return _en_rango(lluvia, 0, math.inf) if lluvia is not None else False


def validar_zona(zona: str, zonas_validas: list) -> bool:
    """La zona existe en la lista de zonas del dataset (sin distinguir mayúsculas)."""
    if not isinstance(zona, str) or not zona.strip():
        return False
    return zona.strip().lower() in [z.lower() for z in zonas_validas]
