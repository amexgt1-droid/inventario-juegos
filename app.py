from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "inventario.json")

# Leer inventario
def leer_inventario():
    if not os.path.exists(JSON_PATH):
        return {}
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Guardar inventario
def guardar_inventario(data):
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Página principal: menú de bases y crear nueva base
@app.route("/", methods=["GET", "POST"])
def index():
    inventario = leer_inventario()
    mensaje = ""
    if request.method == "POST":
        nueva_base = request.form.get("nueva_base").strip()
        if nueva_base in inventario:
            mensaje = f"La base '{nueva_base}' ya existe."
        else:
            inventario[nueva_base] = []
            guardar_inventario(inventario)
            return redirect(url_for("base", base_name=nueva_base))

    return render_template("menu.html", bases=list(inventario.keys()), mensaje=mensaje)

# Página de base: buscar y agregar juegos
@app.route("/base/<base_name>", methods=["GET", "POST"])
def base(base_name):
    inventario = leer_inventario()
    if base_name not in inventario:
        return f"No existe la base {base_name}", 404

    mensaje = ""
    resultado = None

    if request.method == "POST":
        busqueda = request.form.get("buscar").strip()
        for juego in inventario[base_name]:
            if juego["nombre"].lower() == busqueda.lower():
                resultado = juego
                break
        if not resultado:
            mensaje = f"No tenemos '{busqueda}' en {base_name}. Puedes agregarlo abajo."

    return render_template("base.html", base_name=base_name, juegos=inventario[base_name], resultado=resultado, mensaje=mensaje)

# Agregar juego a base
@app.route("/base/<base_name>/agregar", methods=["POST"])
def agregar(base_name):
    inventario = leer_inventario()
    nombre = request.form.get("nombre").strip()
    rareza = request.form.get("rareza").strip()
    cuenta = request.form.get("cuenta").strip()

    inventario[base_name].append({"nombre": nombre, "rareza": rareza, "cuenta": cuenta})
    guardar_inventario(inventario)
    return redirect(url_for("base", base_name=base_name))

if __name__ == "__main__":
    app.run(debug=True)

