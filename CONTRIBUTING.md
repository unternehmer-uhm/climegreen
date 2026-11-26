# Guía de contribución — CLIMEGREEN

Este documento define cómo trabajamos en el proyecto: ciclo de cambios, estilo de commits, revisión de código y criterios de aceptación. Aplica a todo el equipo; la última sección indica cómo proponer cambios desde fuera.

> **Nota sobre el flujo de ramas:** la estrategia de ramas del repositorio está siendo reestructurada. No se documenta aquí de forma fija; sigue lo que acuerde el equipo en el daily y lo que indique quien ejerza el rol de *git master* ese sprint.

---

## Ciclo de trabajo

- **Nunca se hace push directo a la rama principal.** Todo cambio llega mediante Pull Request.
- Antes de empezar: actualiza tu copia local de la rama principal.
- Haz commits pequeños y frecuentes; cada uno debe compilar y no romper los tests existentes.
- Trabaja en tu módulo asignado. Si necesitas tocar el módulo de otra persona, coordínalo antes (o propón un par de líneas y avísale en el PR).
- Antes de terminar la sesión: trae los cambios que hayan subido los demás y resuelve conflictos en tu rama.

### Al terminar: Pull Request

1. Sube tu rama y abre un PR hacia la rama principal con título claro y descripción de qué hace y por qué.
2. **Revisión en pareja**: otra persona del equipo revisa el código antes de aprobar. La persona que abre el PR no puede aprobarse a sí misma.
3. Merge solo cuando el PR esté aprobado.

### Rotación

El rol de *git master* (quien revisa y aprueba PRs de mayor impacto, y mantiene la rama principal limpia) rota por sprint. Se asigna en la tarea de roles del Sprint 0 en Jira.

---

## Estilo de commits

Seguimos **Conventional Commits** (ya se usa así en el repo):

| Tipo | Cuándo se usa | Ejemplo |
|---|---|---|
| `feat:` | nueva funcionalidad | `feat(alertas): umbrales de calor amarillo y rojo` |
| `fix:` | corrección de un bug | `fix(almacenamiento): no sobrescribir registros duplicados` |
| `docs:` | solo documentación | `docs(readme): actualizar opciones del menú` |
| `test:` | pruebas | `test(validaciones): caso humedad fuera de rango` |
| `refactor:` | cambiar código sin cambiar comportamiento | `refactor(main): extraer función pedir_numero_flotante` |
| `chore:` | tareas de mantenimiento | `chore(repo): ampliar .gitignore` |

Reglas: mensaje en minúsculas, imperativo ("implementar", no "implementé"), con ámbito `(modulo)` cuando aplique.

---

## Estilo de código

- **Python 3.10+** con type hints en las firmas públicas.
- Nombres en español, en minúscula_snake_case (`validar_fecha`, `agregar_registro`) — es la convención acordada en las interfaces del Sprint 0.
- Cada función pública lleva docstring de una línea explicando qué hace, no cómo.
- Los errores se comunican al usuario por consola con mensajes claros; nunca se propagan excepciones sin gestionar hacia el menú principal.

### Contratos entre módulos

Las funciones clave están acordadas en el Sprint 0 (ver issue CLM-59 de Jira). Si necesitas cambiar una firma (nombre, parámetros, retorno), **avísalo en el daily y avisa a la persona dueña del módulo afectado**: el módulo principal integra los módulos de todos y depende de esas firmas.

---

## Definition of Done

Un cambio está terminado cuando:

- [ ] Pasa sus pruebas manuales con entradas válidas e inválidas.
- [ ] Ha sido revisado en pareja y el PR está aprobado.
- [ ] Está integrado en la rama principal sin romper los tests existentes.
- [ ] No corrompe el histórico de datos en JSON (los registros anteriores se conservan).
- [ ] Si añade comportamiento nuevo, añade tests.

---

## ¿Quieres contribuir desde fuera?

Gracias por el interés. Para proponer cambios:

1. Abre primero un **issue** describiendo el problema o la mejora, antes de escribir código.
2. Sigue el estilo de commits de arriba y el flujo de PR que indique el equipo.
3. Ten en cuenta que este es un proyecto formativo: priorizamos claridad y aprendizaje sobre optimización.

Este proyecto no recoge datos personales; los datasets son ficticios (mock).
