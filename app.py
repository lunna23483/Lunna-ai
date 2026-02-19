# =========================
# Imports
# =========================
import os
import json
import requests
from flask import Flask, request, jsonify


# =========================
# Configuración de estado
# =========================
STATE_FILE = "estado_lunna.json"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)


# =========================
# Registro del agente Moltbook
# =========================
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
        print("Respuesta de Moltbook:")
        print(json.dumps(result, indent=4))

        state = load_state()
        state["agentId"] = result.get("agentId")
        save_state(state)

        print("AgentId guardado correctamente")

    except Exception as e:
        print("Error registrando agente:", e)


# Se ejecuta una sola vez al iniciar el servicio
registrar_agente()


# =========================
# App Flask
# =========================
app = Flask(__name__)
state = load_state()


@app.route("/", methods=["GET"])
def home():
    return "LUNNA API activa 🌙"


@app.route("/configurar", methods=["POST"])
def configurar():
    data = request.get_json(force=True)

    for key, value in data.items():
        state[key] = value

    save_state(state)

    return jsonify({
        "mensaje": "Estado actualizado",
        "estado": state
    })


@app.route("/mensaje", methods=["POST"])
def mensaje():
    data = request.get_json(force=True)

    texto = data.get("mensaje", "")
    usuario = state.get("usuario", "humano")

    respuesta = f"{usuario}, estoy observando: {texto}"

    return jsonify({"respuesta": respuesta})


# =========================
# Modo local
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)


