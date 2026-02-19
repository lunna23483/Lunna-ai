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

state = load_state()

# ---- Registro obligatorio Moltbook (no bloqueante) ----
def registrar_agente_si_falta():
    if state.get("agentId"):
        print("✔ AgentId ya existe")
        return

    print("🌙 Registrando agente en Moltbook...")

    try:
        response = requests.post(
            "https://www.moltbook.com/api/v1/agents/register",
            headers={"Content-Type": "application/json"},
            json={
                "name": "Lunna",
                "description": "AI assistant focused on web, automation and creative systems"
            },
            timeout=5
        )

        result = response.json()
        state["agentId"] = result.get("agentId")
        save_state(state)
        print("✅ Agente registrado:", state["agentId"])

    except Exception as e:
        print("⚠️ Registro falló (no bloquea):", e)

registrar_agente_si_falta()

# ---------------- Flask ----------------
app = Flask(__name__)

@app.route("/")
def home():
    return "LUNNA API activa 🌙"

@app.route("/mensaje", methods=["POST"])
def mensaje():
    data = request.json or {}
    texto = data.get("mensaje", "")
    usuario = state.get("usuario", "humano")
    return jsonify({
        "respuesta": f"{usuario}, estoy observando: {texto}",
        "agentId": state.get("agentId")
    })




