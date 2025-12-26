# app.py
# Add render_template to your imports
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from chatbot_controller import ChatbotCore

app = Flask(__name__)
CORS(app) # Enable CORS for cross-origin requests

# --- Chatbot Initialization (no change) ---
print("Loading chatbot models...")
chatbot = ChatbotCore()
print("Chatbot models loaded. Server is ready.")


# --- NEW ROUTE ---
# This tells Flask what to do when someone visits the main page ("/")
@app.route("/")
def home():
    # It will look inside the 'templates' folder for 'index.html'
    return render_template("front.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "Empty message received"}), 400
    bot_response = chatbot.handle_message(user_message)
    return jsonify({"response": bot_response})


if __name__ == "__main__":
    app.run(debug=True, port=5000)