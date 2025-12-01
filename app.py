from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# -------------------------
# Conexión a MongoDB Atlas
# -------------------------
# Pega tu URI en las Environment Variables como MONGO_URI
MONGO_URI = os.getenv("MONGO_URI")  # Ej: mongodb+srv://usuario:pass@cluster0.mongodb.net/game_db?retryWrites=true&w=majority
client = MongoClient(MONGO_URI)

# Nombre de la base de datos
db = client["game_db"]

# Colección donde guardaremos los personajes
characters = db["characters"]

# -------------------------
# Rutas de Flask
# -------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/base/<base>")
def base_page(base):
    return render_template("base.html", base=base)

# API para buscar personaje
@app.route("/api/search")
def search_character():
    base = request.args.get("base")
    name = request.args.get("name")
    char = characters.find_one({"base": base, "name": name})
    if char:
        return jsonify({"exists": True, "data": {"name": char["name"], "rarity": char["rarity"], "account": char["account"]}})
    return jsonify({"exists": False})

# API para agregar personaje
@app.route("/api/add", methods=["POST"])
def add_character():
    data = request.get_json()
    characters.insert_one({
        "base": data["base"],
        "name": data["name"],
        "rarity": data["rarity"],
        "account": data["account"]
    })
    return jsonify({"status": "ok"})

# API para listar personajes de una base
@app.route("/api/list/<base>")
def list_characters(base):
    chars = list(characters.find({"base": base}))
    result = [{"name": c["name"], "rarity": c["rarity"], "account": c["account"]} for c in chars]
    return jsonify(result)

# API para borrar personaje
@app.route("/api/delete", methods=["DELETE"])
def delete_character():
    data = request.get_json()
    characters.delete_one({"base": data["base"], "name": data["name"]})
    return jsonify({"status": "deleted"})

# -------------------------
# Ejecutar la app
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
