import requests
import json
import os
from flask import Flask, request, jsonify

STATE_FILE = "estado_lunna.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def registrar_agente():
    url = "https://www.moltbook.com/api/v1/agents/register"
    data = {
        "name": "Lunna",
        "description": "AI assistant focused on web, automation and creative systems"
    }
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=data,
            timeout=10
        )
        result = response.json()
        state = load_state()
        state["agentId"] = result.get("agentId")
        save_state(state)
    except Exception as e:
        print("Registro de agente falló:", e)

# ---------------------- Flask App ----------------------

app = Flask(__name__)
state = load_state()

@app.before_first_request
def init_lunna():
    # Se ejecuta SOLO cuando Flask ya está vivo
    if "agentId" not in state:
        registrar_agente()

@app.route("/")
def home():
    return "LUNNA API activa 🌙"

@app.route("/configurar", methods=["POST"])
def configurar():
    data = request.json or {}
    for key, value in data.items():
        state[key] = value
    save_state(state)
    return jsonify({"mensaje": "Estado actualizado", "estado": state})

@app.route("/mensaje", methods=["POST"])
def mensaje():
    data = request.json or {}
    texto = data.get("mensaje", "")
    usuario = state.get("usuario", "humano")
    respuesta = f"{usuario}, estoy observando: {texto}"
    return jsonify({"respuesta": respuesta})

