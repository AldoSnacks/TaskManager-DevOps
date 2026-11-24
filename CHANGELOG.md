# Registro de cambios

## v1.0.0 - Primera versión estable de TaskManager

### Funcionalidades
- RF01 Registrar tareas con nombre, descripción, prioridad y estado.
- RF02 Consultar la lista de tareas con filtro por estado.
- RF03 Editar tareas existentes.
- RF04 Eliminar tareas con confirmación.
- RF05 Cambiar el estado: Pendiente, En proceso y Terminada.
- RF06 Mostrar mensajes de confirmación y de error.

### Calidad
- 16 pruebas unitarias con pytest (CP01 a CP07).
- Integración continua con GitHub Actions (`ci.yml`).
- Entrega continua con artefacto descargable (`cd.yml`).

### Correcciones
- Se rechazan tareas cuyo nombre es solo espacios.
- Las pruebas de CI ya encuentran el módulo `app` (`pytest.ini`).

### Despliegue
- Configuración para Render (`render.yaml`) con gunicorn y verificación en `/health`.
