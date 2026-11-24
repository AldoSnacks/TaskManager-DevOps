"""TaskManager: sistema web para la gestion de tareas de TechSolutions."""
import os
import sqlite3

from flask import Flask, g, jsonify, render_template, request

ESTADOS = ["Pendiente", "En proceso", "Terminada"]
PRIORIDADES = ["Alta", "Media", "Baja"]


def create_app(database=None):
    app = Flask(__name__)
    app.config["DATABASE"] = database or os.environ.get(
        "DATABASE_PATH", os.path.join(app.root_path, "tareas.db")
    )

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        db = sqlite3.connect(app.config["DATABASE"])
        db.execute(
            """CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL DEFAULT '',
                prioridad TEXT NOT NULL DEFAULT 'Media',
                estado TEXT NOT NULL DEFAULT 'Pendiente',
                creada TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        db.commit()
        db.close()

    init_db()

    def validar(datos, parcial=False):
        """Regresa (datos_limpios, error)."""
        limpio = {}
        if not parcial or "nombre" in datos:
            nombre = str(datos.get("nombre") or "").strip()
            if not nombre:
                return None, "El nombre de la tarea es obligatorio."
            if len(nombre) > 100:
                return None, "El nombre no puede tener mas de 100 caracteres."
            limpio["nombre"] = nombre
        if not parcial or "descripcion" in datos:
            limpio["descripcion"] = str(datos.get("descripcion") or "").strip()
        if not parcial or "prioridad" in datos:
            prioridad = datos.get("prioridad") or "Media"
            if prioridad not in PRIORIDADES:
                return None, "Prioridad no valida. Usa: Alta, Media o Baja."
            limpio["prioridad"] = prioridad
        if not parcial or "estado" in datos:
            estado = datos.get("estado") or "Pendiente"
            if estado not in ESTADOS:
                return None, "Estado no valido. Usa: Pendiente, En proceso o Terminada."
            limpio["estado"] = estado
        return limpio, None

    def buscar(tarea_id):
        fila = get_db().execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,)).fetchone()
        return dict(fila) if fila else None

    @app.get("/")
    def index():
        return render_template("index.html", estados=ESTADOS, prioridades=PRIORIDADES)

    @app.get("/health")
    def health():
        get_db().execute("SELECT 1")
        return jsonify({"status": "ok"})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
