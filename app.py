from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

# Funciones para leer y guardar inventario
def cargar_inventario():
    with open("inventario.json", "r", encoding="utf-8") as file:
        return json.load(file)

def guardar_inventario(data):
    with open("inventario.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Página pública
@app.route("/")
def index():
    inventario = cargar_inventario()
    return render_template("index.html", inventario=inventario)

# Panel de administración
@app.route("/admin", methods=["GET", "POST"])
def admin():
    inventario = cargar_inventario()

    if request.method == "POST":
        nombre = request.form["nombre"]
        rareza = request.form["rareza"]
        cuenta = request.form["cuenta"]

        inventario.append({
            "nombre": nombre,
            "rareza": rareza,
            "cuenta": cuenta
        })

        guardar_inventario(inventario)
        return redirect("/admin")

    return render_template("admin.html", inventario=inventario)

if __name__ == "__main__":
    app.run(debug=True)
