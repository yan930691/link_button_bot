# app.py
import os
import threading
from flask import Flask, jsonify
from bot import main as bot_main

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Link Button Maker Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

def run_bot():
    bot_main()

if __name__ == "__main__":
    # Bot ကို သီးခြား thread နဲ့ စတင်
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Flask server ကို port $PORT မှာ စတင်
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
