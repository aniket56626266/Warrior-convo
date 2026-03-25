import os, requests, time
from flask import Flask, render_template_string, request, redirect
from threading import Thread

app = Flask(__name__)
is_running = False
logs = []

# --- BRANDING ---
OWNER_NAME = "WARRIOR" 
PANEL_TITLE = f"🛡️ {OWNER_NAME} UNLIMITED CONVO SERVER 🛡️"

# Warrior Aggressive Red-Black Theme
HTML_UI = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { background: #000; color: #ff0000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; padding: 20px; }
        .container { border: 2px solid #ff0000; padding: 25px; border-radius: 20px; background: #0a0a0a; max-width: 450px; margin: auto; box-shadow: 0 0 30px #ff0000; }
        .warrior-brand { font-size: 26px; font-weight: 900; letter-spacing: 2px; margin-bottom: 20px; text-shadow: 0 0 15px #ff0000; color: #fff; }
        input, textarea, select { width: 90%; margin: 10px 0; background: #111; color: #fff; border: 1px solid #ff0000; padding: 12px; border-radius: 8px; font-size: 14px; outline: none; }
        .btn { width: 95%; padding: 15px; font-weight: bold; cursor: pointer; border-radius: 8px; border: none; font-size: 16px; text-transform: uppercase; transition: 0.3s; }
        .btn-start { background: #ff0000; color: #fff; box-shadow: 0 0 15px #ff0000; }
        .btn-stop { background: #333; color: #fff; margin-top: 15px; }
        .logs { text-align: left; background: #000; padding: 15px; height: 200px; overflow-y: auto; border: 1px dashed #ff0000; margin-top: 20px; font-size: 12px; color: #00ff00; border-radius: 8px; }
        .status-bar { font-size: 12px; color: #fff; margin-bottom: 15px; background: #222; padding: 5px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="warrior-brand">{{ title }}</div>
        <div class="status-bar">SYSTEM STATUS: <span style="color:{{ 'lime' if running else 'red' }};">{{ 'ACTIVE 24/7' if running else 'OFFLINE' }}</span></div>
        <form action="/start" method="post">
            <select name="method">
                <option value="token">METHOD 1: TOKEN (GRAPH API - BEST)</option>
                <option value="cookie">METHOD 2: COOKIE (MBASIC - SLOW)</option>
            </select>
            <input name="access_key" placeholder="Paste Token/Cookie Here" required>
            <input name="target" placeholder="Target Numeric ID" required>
            <input name="hater_name" placeholder="Hater Name (Jo message ke aage aayega)">
            <input name="delay" type="number" value="20" required>
            <textarea name="msgs" placeholder="Messages (One per line)" rows="5" required></textarea>
            <button type="submit" class="btn btn-start">ACTIVATE WARRIOR ATTACK</button>
        </form>
        <a href="/stop"><button class="btn btn-stop">STOP ATTACK</button></a>
        <div class="logs">
            <strong>WARRIOR SYSTEM LOGS:</strong><br>
            {% for log in logs %} <p style="margin:4px 0; border-bottom: 1px solid #1a1a1a;">{{ log }}</p> {% endfor %}
        </div>
    </div>
    <p style="font-size: 11px; color: #555; margin-top: 20px;">© 2026 WARRIOR PRIVATE BOT - UNLIMITED EDITION</p>
</body>
</html>
'''

def run_bot(method, access_key, target, name, delay, msgs):
    global is_running, logs
    is_running = True
    while is_running:
        for m in msgs:
            if not is_running: break
            full_msg = f"{name} {m.strip()}" if name else m.strip()
            
            try:
                if method == "token":
                    url = f"https://graph.facebook.com/v17.0/t_{target}/messages"
                    r = requests.post(url, data={'message': full_msg, 'access_token': access_key})
                else:
                    url = f"https://mbasic.facebook.com/messages/send/?tids={target}"
                    r = requests.post(url, cookies={'cookie': access_key}, data={'body': full_msg, 'send': 'Send', 'www_form_post': '1'})
                
                if r.status_code == 200:
                    logs.append(f"✅ SENT: {full_msg[:15]}...")
                else:
                    logs.append(f"❌ FAILED: Check Token/Cookie")
            except:
                logs.append("🌐 CONNECTION ERROR - RETRYING")
            
            time.sleep(int(delay))
        logs.append("--- Round Complete, Restarting ---")

@app.route('/')
def index():
    return render_template_string(HTML_UI, logs=logs[-15:], running=is_running, title=PANEL_TITLE)

@app.route('/start', methods=['POST'])
def start():
    Thread(target=run_bot, args=(request.form['method'], request.form['access_key'], request.form['target'], request.form['hater_name'], request.form['delay'], request.form['msgs'].split('\n'))).start()
    return redirect('/')

@app.route('/stop')
def stop():
    global is_running
    is_running = False
    logs.append("🛑 ATTACK STOPPED BY WARRIOR.")
    return redirect('/')

if __name__ == "__main__":
    # Render ke liye port 10000 zaroori hai
    app.run(host='0.0.0.0', port=10000)
                  
