"""Módulo principal de la aplicación CLIMEGREEN."""

from typing import Any

# Intentamos importar los módulos del equipo si ya tienen funciones definidas
try:
    import validaciones
except ImportError:
    validaciones = None

try:
    import almacenamiento
except ImportError:
    almacenamiento = None

try:
    import alertas
except ImportError:
    alertas = None


def pedir_texto_obligatorio(etiqueta: str) -> str:
    """Pide un texto no vacío con reintento."""
    while True:
        valor = input(etiqueta).strip()
        if valor:
            return valor
        print("Error: este campo no puede quedar vacío. Inténtalo de nuevo.")


def pedir_numero_flotante(etiqueta: str) -> float:
    """Pide un número decimal con reintento ante letras o campos vacíos."""
    while True:
        entrada = input(etiqueta).strip().replace(",", ".")
        if not entrada:
            print("Error: este campo no puede quedar vacío. Inténtalo de nuevo.")
            continue
        try:
            return float(entrada)
        except ValueError:
            print("Error: debes introducir un valor numérico (ej. 22.5). Inténtalo de nuevo.")


def validar_registro(registro: dict[str, Any]) -> tuple[bool, str]:
    """Conecta con validaciones.py de SaraCo (CLM-23) o usa validación base."""
    if validaciones and hasattr(validaciones, "validar_registro"):
        return validaciones.validar_registro(registro)
    return True, "Validación provisional OK"


def guardar_registro(registro: dict[str, Any]) -> None:
    """Conecta con agregar_registro de Doramas (CLM-24) o usa respaldo provisional."""
    if almacenamiento and hasattr(almacenamiento, "agregar_registro"):
        almacenamiento.agregar_registro(registro)
    else:
        print("[Pendiente almacenamiento] Registro preparado para guardar:", registro)


def evaluar_alertas(registro: dict[str, Any]) -> list[str]:
    """Conecta con alertas.py de Susana (CLM-25) o usa respaldo provisional."""
    if alertas and hasattr(alertas, "evaluar_alertas"):
        resultado = alertas.evaluar_alertas(registro)
        if isinstance(resultado, list):
            return resultado
        return [str(resultado)] if resultado else []
    return []


def validar_zona_entrada(zona: str) -> tuple[bool, str]:
    """Conecta con validar_zona de SaraCo o aplica validación provisional."""
    if validaciones and hasattr(validaciones, "validar_zona"):
        resultado = validaciones.validar_zona(zona)
        if isinstance(resultado, tuple) and len(resultado) == 2:
            return bool(resultado[0]), str(resultado[1])
        return bool(resultado), "Zona no válida."
    if not zona.strip():
        return False, "La zona no puede estar vacía."
    return True, "Zona válida"


def obtener_registros_por_zona(zona: str) -> list[dict[str, Any]]:
    """Conecta con filtrar_por_zona de Doramas o devuelve lista vacía provisional."""
    if almacenamiento and hasattr(almacenamiento, "filtrar_por_zona"):
        datos = almacenamiento.filtrar_por_zona(zona)
        if isinstance(datos, list):
            return datos
    return []


def imprimir_tabla_registros(zona: str, registros: list[dict[str, Any]]) -> None:
    """Imprime los registros filtrados en formato de tabla legible por consola."""
    print(f"\n--- Registros para la zona: {zona} ---")
    if not registros:
        print("No hay mediciones registradas para esta zona.")
        return

    cabeceras = ["Fecha", "Zona", "Temp (°C)", "Hum (%)", "Viento (km/h)", "Lluvia (mm)"]
    filas: list[list[str]] = []

    for item in registros:
        filas.append([
            str(item.get("fecha", "")),
            str(item.get("zona", zona)),
            str(item.get("temperatura", "")),
            str(item.get("humedad", "")),
            str(item.get("viento", "")),
            str(item.get("lluvia", "")),
        ])

    anchos = [
        max(len(cabeceras[i]), *(len(fila[i]) for fila in filas))
        for i in range(len(cabeceras))
    ]

    linea_sep = "+" + "+".join("-" * (ancho + 2) for ancho in anchos) + "+"
    encabezado = "|" + "|".join(f" {cabeceras[i]:<{anchos[i]}} " for i in range(len(cabeceras))) + "|"

    print(linea_sep)
    print(encabezado)
    print(linea_sep)
    for fila in filas:
        print("|" + "|".join(f" {fila[i]:<{anchos[i]}} " for i in range(len(cabeceras))) + "|")
    print(linea_sep)


def opcion_registrar() -> None:
    """Flujo completo de la opción 1: Registrar medición climática."""
    print("\n--- Registrar nueva medición en CLIMEGREEN ---")
    while True:
        fecha = pedir_texto_obligatorio("Fecha (YYYY-MM-DD): ")
        zona = pedir_texto_obligatorio("Zona / Distrito: ")
        temperatura = pedir_numero_flotante("Temperatura (°C): ")
        humedad = pedir_numero_flotante("Humedad (%): ")
        viento = pedir_numero_flotante("Viento (km/h): ")
        lluvia = pedir_numero_flotante("Lluvia (mm): ")

        registro = {
            "fecha": fecha,
            "zona": zona,
            "temperatura": temperatura,
            "humedad": humedad,
            "viento": viento,
            "lluvia": lluvia,
        }

        es_valido, mensaje = validar_registro(registro)
        if not es_valido:
            print(f"\nDatos no válidos: {mensaje}")
            reintentar = input("¿Quieres volver a introducir los datos? (s/n): ").strip().lower()
            if reintentar == "s":
                continue
            print("Registro cancelado.")
            return

        try:
            guardar_registro(registro)
        except Exception as error:
            print(f"\nError al guardar el registro: {error}")
            return

        lista_alertas = evaluar_alertas(registro)
        print("\nRegistro completado correctamente.")
        if lista_alertas:
            print("Alertas generadas:")
            for alerta in lista_alertas:
                print(f" - {alerta}")
        else:
            print("Sin alertas activas para esta medición.")
        break


def opcion_consultar_por_zona() -> None:
    """Flujo de la opción 2: Consultar por zona con salida en tabla."""
    print("\n--- Consultar mediciones por zona ---")
    zona = pedir_texto_obligatorio("Introduce la zona a consultar: ")

    es_valida, mensaje = validar_zona_entrada(zona)
    if not es_valida:
        print(f"\nAviso: {mensaje} Volviendo al menú principal.")
        return

    try:
        registros = obtener_registros_por_zona(zona)
    except Exception as error:
        print(f"\nError al consultar los registros: {error}")
        return

    imprimir_tabla_registros(zona, registros)


def ver_historico_stub() -> None:
    print("\n[Pendiente] Opción 3: Ver histórico.")


def mostrar_menu() -> None:
    print("\n=== CLIMEGREEN ===")
    print("1) Registrar")
    print("2) Consultar por zona")
    print("3) Histórico")
    print("4) Salir")


def main() -> None:
    while True:
        mostrar_menu()
        try:
            opcion = input("Selecciona una opción (1-4): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSalida limpia de CLIMEGREEN. ¡Hasta pronto!")
            break

        if opcion == "1":
            opcion_registrar()
        elif opcion == "2":
            opcion_consultar_por_zona()
        elif opcion == "3":
            ver_historico_stub()
        elif opcion == "4":
            print("\nSalida limpia de CLIMEGREEN. ¡Hasta pronto!")
            break
        else:
            print("\nOpción no válida. Introduce un número entre 1 y 4.")


if __name__ == "__main__":
    main()
