# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y [Versionado Semántico](https://semver.org/lang/es/). Este proyecto está en fase MVP: hasta la versión `1.0.0` las interfaces entre módulos pueden cambiar.

## [No publicado]

### Previsto (roadmap)

- Lógica de umbrales de alerta (amarillo/rojo) por calor, viento y lluvia.
- Persistencia JSON, filtrado por zona y control de duplicados.
- Dataset inicial (mock) en JSON.
- Batería de pruebas automatizadas.
- Estadísticas básicas por zona (medias diarias/semanales/mensuales) — Sprint 2.
- Refactorización final y retrospectiva — Sprint 2.

> Nota: el detalle por módulo se consulta en el tablero de Jira (proyecto CLM), no aquí, para no duplicar fuentes de verdad.

## [0.2.0] - 2026-11-26

### Añadido

- Menú principal de consola: registro guiado con reintentos ante entradas inválidas, consulta por zona con salida en tabla y salida limpia.
- `README.md` reformateado a Markdown completo (tablas, bloques de código, estructura del proyecto).
- `CONTRIBUTING.md` con el ciclo de trabajo, estilo de commits y Definition of Done del equipo.
- `.gitignore` ampliado: cachés de Python, logs generados, IDEs y secretos locales.
- `.env.example` como plantilla para `python-dotenv`.
- `CHANGELOG.md` (este archivo) y `LICENSE` (MIT).

### Corregido

- El README documentaba un menú de 3 opciones mientras el código del trabajo en curso contempla 4; pendiente de alinear.

## [0.1.1] - 2026-11-24

### Cambiado

- Renombrado el proyecto de WEATHER CLI a **CLIMEGREEN**.
- Revisión del `README.md` y `requirements.txt` iniciales.

## [0.1.0] - 2026-11-24

### Añadido

- Repositorio inicial: `README.md`, `requirements.txt`, `.gitignore`.
- Esqueleto inicial del proyecto con las firmas de validación acordadas (PR #2).
