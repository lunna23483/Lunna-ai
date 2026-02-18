import requests
import json
import os

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
        response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
        result = response.json()
        print("Respuesta de Moltbook:", json.dumps(result, indent=4))
        
        # Guardamos el agentId en el estado
        state = load_state()
        state["agentId"] = result.get("agentId")
        save_state(state)
        print("AgentId guardado en estado_lunna.json")
    except Exception as e:
        print("Error registrando agente:", e)

# Registrar agente antes de iniciar el servidor
registrar_agente()

# ---------------------- Tu Flask App ----------------------
from flask import Flask, request, jsonify

app = Flask(__name__)
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

