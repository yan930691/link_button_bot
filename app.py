# app.py
import os
from threading import Thread
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Link Button Maker Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

def run_bot():
    from bot import main
    main()

if __name__ == "__main__":
    # Bot ကို daemon thread နဲ့ run ပါ
    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
