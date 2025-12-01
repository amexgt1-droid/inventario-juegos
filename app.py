from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# ---------------------------
# CONEXIÓN A MONGO
# ---------------------------
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["game_db"]
characters = db.characters

# ---------------------------
# RUTAS HTML
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/base/<base>")
def base_page(base):
    return render_template("base.html", base=base)

# ---------------------------
# API
# ---------------------------

@app.get("/api/search")
def search():
    base = request.args.get("base")
    name = request.args.get("name")

    char = characters.find_one({"base": base, "name": name})

    if not char:
        return jsonify({"exists": False})

    char["_id"] = str(char["_id"])
    return jsonify({"exists": True, "data": char})


@app.post("/api/add")
def add_character():
    data = request.json
    new_char = {
        "base": data["base"],
        "name": data["name"],
        "rarity": data["rarity"],
        "account": data["account"]
    }
    characters.insert_one(new_char)
    return jsonify({"success": True})


@app.get("/api/list/<base>")
def list_characters(base):
    list_chars = []
    for char in characters.find({"base": base}):
        char["_id"] = str(char["_id"])
        list_chars.append(char)
    return jsonify(list_chars)


@app.delete("/api/delete")
def delete_char():
    data = request.json
    characters.delete_one({
        "base": data["base"],
        "name": data["name"]
    })
    return jsonify({"success": True})


# ---------------------------
# RUN
# ---------------------------
if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
