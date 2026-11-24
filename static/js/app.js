const API = "/api/tareas";
const form = document.getElementById("form-tarea");
const mensaje = document.getElementById("mensaje");
const lista = document.getElementById("lista-tareas");
const filtro = document.getElementById("filtro-estado");
const campos = ["nombre", "descripcion", "prioridad", "estado"];
let tareas = [];

function mostrarMensaje(texto, tipo) {
  mensaje.textContent = texto;
  mensaje.className = tipo;
}

async function peticion(url, opciones = {}) {
  const resp = await fetch(url, { headers: { "Content-Type": "application/json" }, ...opciones });
  const datos = await resp.json();
  if (!resp.ok) throw new Error(datos.error || "Error inesperado");
  return datos;
}

function limpiarFormulario() {
  form.reset();
  document.getElementById("tarea-id").value = "";
  document.getElementById("prioridad").value = "Media";
  document.getElementById("titulo-form").textContent = "Nueva tarea";
  document.getElementById("btn-cancelar").hidden = true;
}

function crearElemento(tarea) {
  const li = document.createElement("li");
  li.className = "tarea";
  li.dataset.id = tarea.id;
  const h3 = document.createElement("h3");
  h3.textContent = tarea.nombre;
  const p = document.createElement("p");
  p.textContent = tarea.descripcion || "Sin descripción";
  const etiquetas = document.createElement("div");
  etiquetas.className = "etiquetas";
  etiquetas.innerHTML = `<span class="etiqueta p-${tarea.prioridad}">Prioridad ${tarea.prioridad}</span>`;

  const controles = document.createElement("div");
  controles.className = "controles";
  const selEstado = document.createElement("select");
  selEstado.setAttribute("aria-label", "Cambiar estado");
  window.ESTADOS.forEach((e) => selEstado.add(new Option(e, e, false, e === tarea.estado)));
  selEstado.addEventListener("change", () => cambiarEstado(tarea.id, selEstado.value));
  const btnEditar = document.createElement("button");
  btnEditar.textContent = "Editar";
  btnEditar.addEventListener("click", () => editar(tarea));
  const btnEliminar = document.createElement("button");
  btnEliminar.textContent = "Eliminar";
  btnEliminar.className = "peligro";
  btnEliminar.addEventListener("click", () => eliminar(tarea));
  controles.append(selEstado, btnEditar, btnEliminar);

  li.append(h3, p, etiquetas, controles);
  return li;
}

function pintar() {
  const visibles = tareas.filter((t) => !filtro.value || t.estado === filtro.value);
  lista.innerHTML = "";
  if (!visibles.length) {
    lista.innerHTML = '<li class="vacio">No hay tareas registradas.</li>';
  }
  visibles.forEach((t) => lista.appendChild(crearElemento(t)));
  const cuenta = (e) => tareas.filter((t) => t.estado === e).length;
  document.getElementById("resumen").textContent =
    `Total: ${tareas.length} | Pendientes: ${cuenta("Pendiente")} | En proceso: ${cuenta("En proceso")} | Terminadas: ${cuenta("Terminada")}`;
}

async function cargar() {
  tareas = await peticion(API);
  pintar();
}

function editar(tarea) {
  document.getElementById("tarea-id").value = tarea.id;
  campos.forEach((c) => (document.getElementById(c).value = tarea[c]));
  document.getElementById("titulo-form").textContent = "Editar tarea";
  document.getElementById("btn-cancelar").hidden = false;
  document.getElementById("nombre").focus();
}

async function cambiarEstado(id, estado) {
  try {
    const r = await peticion(`${API}/${id}`, { method: "PUT", body: JSON.stringify({ estado }) });
    mostrarMensaje(`Estado actualizado a "${r.tarea.estado}".`, "ok");
    await cargar();
  } catch (e) { mostrarMensaje(e.message, "error"); }
}

async function eliminar(tarea) {
  if (!confirm(`¿Eliminar la tarea "${tarea.nombre}"?`)) return;
  try {
    const r = await peticion(`${API}/${tarea.id}`, { method: "DELETE" });
    mostrarMensaje(r.mensaje, "ok");
    await cargar();
  } catch (e) { mostrarMensaje(e.message, "error"); }
}

form.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const datos = Object.fromEntries(campos.map((c) => [c, document.getElementById(c).value]));
  if (!datos.nombre.trim()) {
    mostrarMensaje("El nombre de la tarea es obligatorio.", "error");
    return;
  }
  const id = document.getElementById("tarea-id").value;
  try {
    const r = id
      ? await peticion(`${API}/${id}`, { method: "PUT", body: JSON.stringify(datos) })
      : await peticion(API, { method: "POST", body: JSON.stringify(datos) });
    mostrarMensaje(r.mensaje, "ok");
    limpiarFormulario();
    await cargar();
  } catch (e) { mostrarMensaje(e.message, "error"); }
});

document.getElementById("btn-cancelar").addEventListener("click", limpiarFormulario);
filtro.addEventListener("change", pintar);
cargar();
