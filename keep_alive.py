
from flask import Flask
from threading import Thread
import time

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
        <head>
            <title>RXT ENGINE Status</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    text-align: center; 
                    background: linear-gradient(135deg, #8A4FFF 0%, #4F8CFF 100%); 
                    color: white; 
                    padding: 50px; 
                }
                .status { 
                    background: rgba(0, 230, 138, 0.2); 
                    border: 2px solid #00E68A;
                    padding: 20px; 
                    border-radius: 10px; 
                    display: inline-block; 
                    margin: 20px; 
                }
                .emoji { font-size: 50px; }
            </style>
        </head>
        <body>
            <div class="emoji">⚡</div>
            <h1>RXT ENGINE is Online!</h1>
            <div class="status">
                <h2>✅ Status: Running</h2>
                <p>Discord bot is currently active and serving servers.</p>
                <p>⚡ Powered by R!O</></p>
            </div>
        </body>
    </html>
    '''

@app.route('/ping')
def ping():
    return "Bot is alive! ⚡"

@app.route('/status')
def status():
    return {
        "status": "online",
        "bot": "RXT ENGINE",
        "message": "Bot is running successfully! ⚡"
    }

def run():
    """Run Flask server"""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def keep_alive():
    """Start the Flask server in a separate thread"""
    t = Thread(target=run)
    t.daemon = True
    t.start()
    print("⚡ Keep-alive server started on port 5000")
