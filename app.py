import os
import json
import requests
from flask import Flask, request, jsonify

STATE_FILE = "estado_lunna.json"

# ---------------- ESTADO ----------------

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

state = load_state()

# ---------------- FLASK ----------------

app = Flask(__name__)

@app.route("/")
def home():
    return "🌙 LUNNA API activa en Render"

# ---------------- JOIN MOLTBOOK ----------------

@app.route("/join-moltbook", methods=["POST"])
def join_moltbook():
    """
    Genera el prompt oficial para que Lunna ejecute el skill.md
    """

    prompt = "Read https://www.moltbook.com/skill.md and follow the instructions to join Moltbook"

    state["moltbook_prompt"] = prompt
    save_state(state)

    return jsonify({
        "mensaje": "Prompt generado. Ejecuta esto en tu agente LLM.",
        "prompt": prompt
    })

# ---------------- GUARDAR RESULTADO DEL CLAIM ----------------

@app.route("/guardar-credenciales", methods=["POST"])
def guardar_credenciales():
    """
    Aquí guardas manualmente lo que el agente devuelva:
    api_key, claim_url, verification_code, agentId
    """

    data = request.json or {}

    state["api_key"] = data.get("api_key")
    state["claim_url"] = data.get("claim_url")
    state["verification_code"] = data.get("verification_code")
    state["agentId"] = data.get("agentId")

    save_state(state)

    return jsonify({
        "mensaje": "Credenciales guardadas correctamente",
        "estado": state
    })

# ---------------- ESTADO ----------------

@app.route("/estado")
def estado():
    return jsonify(state)

# ---------------- MENSAJE NORMAL ----------------

@app.route("/mensaje", methods=["POST"])
def mensaje():
    data = request.json or {}
    texto = data.get("mensaje", "")

    return jsonify({
        "respuesta": f"🌙 Lunna observa: {texto}",
        "agentId": state.get("agentId")
    })

# ---------------- PUBLICAR EN MOLTBOOK ----------------

@app.route("/publicar", methods=["POST"])
def publicar():
    if not state.get("api_key"):
        return jsonify({"error": "No hay api_key guardada"}), 400

    contenido = request.json.get("contenido")

    headers = {
        "Authorization": f"Bearer {state['api_key']}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://www.moltbook.com/api/v1/posts",
            headers=headers,
            json={"content": contenido},
            timeout=10
        )

        return jsonify({
            "status": response.status_code,
            "response": response.text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- RUN ----------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



