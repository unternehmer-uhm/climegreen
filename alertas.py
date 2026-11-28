"""Módulo de evaluación de alertas climáticas (calor, viento y lluvia)."""

REGLAS_POR_VARIABLE: dict[str, tuple[tuple[float, float, str, str, str], ...]] = {
    "temperatura": (
        (40.0, 40.0, "ROJA", "CALOR EXTREMO", "°C"),
        (35.0, 35.0, "AMARILLA", "CALOR", "°C"),
    ),
    "viento": (
        (70.0, 70.0, "ROJA", "VIENTO FUERTE", "km/h"),
        (50.0, 50.0, "NARANJA", "VIENTO", "km/h"),
    ),
    "lluvia": (
        (40.0, 40.0, "ROJA", "LLUVIA TORRENCIAL", "mm"),
        (15.0, 15.0, "AMARILLA", "LLUVIA INTENSA", "mm"),
    ),
}


def evaluar_alertas(
    temperatura: float,
    viento: float,
    lluvia: float,
) -> list[str]:
    """Evalúa umbrales de riesgo y devuelve una lista de alertas activadas."""
    valores = {
        "temperatura": temperatura,
        "viento": viento,
        "lluvia": lluvia,
    }
    alertas: list[str] = []

    for variable, reglas in REGLAS_POR_VARIABLE.items():
        valor = valores[variable]
        for umbral, umbral_texto, nivel, motivo, unidad in reglas:
            if valor >= umbral:
                alertas.append(
                    f"ALERTA {nivel} POR {motivo} "
                    f"({valor} {unidad} >= {umbral_texto:g} {unidad})"
                )
                break

    return alertas


def evaluar_registro(registro: dict) -> list[str]:
    """Evalúa alertas a partir de un diccionario de registro climático."""
    return evaluar_alertas(
        temperatura=float(registro["temperatura"]),
        viento=float(registro["viento"]),
        lluvia=float(registro["lluvia"]),
    )


def formatear_bloque_alertas(alertas: list[str], zona: str | None = None) -> str:
    """Devuelve un texto listo para mostrar en consola cuando hay alertas."""
    if not alertas:
        return "Sin alertas meteorológicas activadas."

    encabezado = f"Protocolos activados en {zona}:" if zona else "Protocolos activados:"
    lineas = [encabezado] + [f"  - {alerta}" for alerta in alertas]
    return "\n".join(lineas)
