from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_MODEL = "qwen2.5:1.5b"
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message."})

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": user_message,
                "stream": False
            },
            timeout=180
        )
        response.raise_for_status()
        ai_reply = response.json().get("response", "No response from AI.")
    except Exception as e:
        ai_reply = f"Ollama error: {e}"

    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)
