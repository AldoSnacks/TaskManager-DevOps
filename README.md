# TaskManager-DevOps

Sistema web para la gestión de tareas de **TechSolutions**, desarrollado aplicando las fases del ciclo de vida DevOps con GitHub (Projects, Issues, Git, Actions y Releases).

**Equipo:** Aldo Misael Leal Palafox · Carlos Manuel Ojeda Hernández

[![Integracion Continua](https://github.com/AldoSnacks/TaskManager-DevOps/actions/workflows/ci.yml/badge.svg)](https://github.com/AldoSnacks/TaskManager-DevOps/actions/workflows/ci.yml)

- **Aplicación publicada (Render):** https://taskmanager-devops-23a0.onrender.com
- **Versión estable:** [v1.0.0 – Primera versión estable de TaskManager](https://github.com/AldoSnacks/TaskManager-DevOps/releases/tag/v1.0.0)
- **Tablero del proyecto:** GitHub Projects "TaskManager-DevOps"

> En el plan gratuito de Render la instancia se suspende tras unos minutos sin uso; la primera visita puede tardar hasta 50 segundos y las tareas guardadas en SQLite se reinician cuando el servicio se reinicia (ver incidentes en Issues).

## Funcionalidades

| Código | Funcionalidad | Descripción |
|---|---|---|
| RF01 | Registrar tareas | Agregar nuevas tareas con nombre, descripción, prioridad y estado. |
| RF02 | Consultar tareas | Mostrar todas las tareas registradas (con filtro por estado). |
| RF03 | Editar tareas | Modificar la información de una tarea. |
| RF04 | Eliminar tareas | Eliminar tareas existentes. |
| RF05 | Cambiar estado | Pendiente, En proceso o Terminada. |
| RF06 | Asignar prioridad | Alta, Media o Baja. |

## Tecnologías

- Backend: Python 3.12 + Flask
- Frontend: HTML, CSS y JavaScript
- Base de datos: SQLite
- Pruebas: Pytest
- CI/CD: GitHub Actions (`ci.yml` y `cd.yml`)
- Despliegue: Render (`render.yaml`, servidor `gunicorn`)

## Ejecutar en local

```bash
git clone https://github.com/AldoSnacks/TaskManager-DevOps.git
cd TaskManager-DevOps
pip install -r requirements.txt
python app.py          # http://127.0.0.1:5000
pytest -v              # pruebas unitarias
```

## API

| Método | Ruta | Uso |
|---|---|---|
| GET | `/api/tareas` | Consultar tareas |
| POST | `/api/tareas` | Registrar tarea |
| GET | `/api/tareas/<id>` | Consultar una tarea |
| PUT | `/api/tareas/<id>` | Editar tarea o cambiar estado |
| DELETE | `/api/tareas/<id>` | Eliminar tarea |
| GET | `/health` | Monitoreo de disponibilidad |

## Historias de usuario

**HU1. Registrar tareas.** Como usuario del sistema, quiero registrar nuevas tareas para organizar mis actividades.
- Permite ingresar el nombre de la tarea.
- Permite agregar una descripción.
- Permite seleccionar una prioridad.
- Guarda la tarea.
- Muestra un mensaje de confirmación.

**HU2. Cambiar estado de tareas.** Como usuario, quiero cambiar el estado de una tarea para conocer su progreso.
- Permite seleccionar Pendiente, En proceso y Terminada.
- El cambio se refleja en el listado de tareas.

**HU3. Consultar tareas.** Como usuario, quiero ver todas las tareas registradas para saber qué está pendiente y qué está terminado.
- Muestra nombre, descripción, prioridad y estado de cada tarea.
- Muestra el total de tareas por estado.
- Permite filtrar el listado por estado.

**HU4. Editar tareas.** Como usuario, quiero modificar una tarea para corregir o actualizar su información.
- Permite cambiar nombre, descripción, prioridad y estado.
- No permite dejar el nombre vacío.
- Muestra un mensaje de confirmación y el listado actualizado.

**HU5. Eliminar tareas.** Como usuario, quiero eliminar tareas que ya no son necesarias para mantener la lista ordenada.
- Pide confirmación antes de eliminar.
- La tarea desaparece del listado.

**HU6. Asignar prioridad.** Como usuario, quiero clasificar las tareas como Alta, Media o Baja para atender primero lo importante.
- Solo acepta Alta, Media o Baja.
- La prioridad se muestra con un color distinto en el listado.
