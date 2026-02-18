from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

STATE_FILE = "estado_lunna.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

state = load_state()

@app.route("/")
def home():
    return "LUNNA API activa 🌙"

@app.route("/configurar", methods=["POST"])
def configurar():
    data = request.json
    for key, value in data.items():
        state[key] = value
    save_state(state)
    return jsonify({"mensaje": "Estado actualizado", "estado": state})

@app.route("/mensaje", methods=["POST"])
def mensaje():
    data = request.json
    texto = data.get("mensaje", "")

    usuario = state.get("usuario", "humano")

    respuesta = f"{usuario}, estoy observando: {texto}"

    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
