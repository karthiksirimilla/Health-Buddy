from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename
from ai_derma_bot.utils import detect_and_respond
from gtts import gTTS
from flask_cors import CORS
import os
app = Flask(__name__)

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Chat Page (BotPress Chat)
@app.route("/chat")
def chat_page():
    return render_template("chat.html")

# Chat with the DermaBot
@app.route('/dermabot')
def chat():
    return render_template('chat.html')

# Voice-Based Sickness Detection Page
@app.route("/voice")
def voice_page():
    return render_template("voice.html")

# Voice-Based Sickness Detection Logic
@app.route("/voice-check", methods=["POST"])
def voice_analysis():
    try:
        sickness_status = "Likely Sick (low energy, slow speech, low pitch)"
        return jsonify({"status": sickness_status})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Skin disease detection page
@app.route("/derma_bot")
def skin_disease_page():
    return render_template("derma_bot.html")

UPLOAD_FOLDER = "temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/dermabot-detect", methods=["POST"])
def dermabot_detect():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = secure_filename(file.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(image_path)

    prediction_data = detect_and_respond(image_path)  # This returns dict

    return jsonify(prediction_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)

