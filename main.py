"""Punto de entrada inicial para el esqueleto del proyecto."""


def main() -> None:
    print("Esqueleto listo: main.py iniciado correctamente.")


if __name__ == "__main__":
    main()
    """Módulo principal de la aplicación climática del Ayuntamiento."""


def registrar_stub() -> None:
    print("\n[Pendiente] Opción 1: Registrar medición (Tarea 4.3).")


def consultar_zona_stub() -> None:
    print("\n[Pendiente] Opción 2: Consultar por zona (Tarea 4.4).")


def ver_historico_stub() -> None:
    print("\n[Pendiente] Opción 3: Ver histórico.")


def mostrar_menu() -> None:
    print("\n=== APP CLIMÁTICA - AYUNTAMIENTO ===")
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
            print("\nSalida limpia de la aplicación. ¡Hasta pronto!")
            break

        if opcion == "1":
            registrar_stub()
        elif opcion == "2":
            consultar_zona_stub()
        elif opcion == "3":
            ver_historico_stub()
        elif opcion == "4":
            print("\nSalida limpia de la aplicación. ¡Hasta pronto!")
            break
        else:
            print("\nOpción no válida. Introduce un número entre 1 y 4.")


if __name__ == "__main__":
    main()
