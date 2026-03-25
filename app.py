import os, requests, time
from flask import Flask, render_template_string, request, redirect
from threading import Thread

app = Flask(__name__)
is_running = False
logs = []

# --- BRANDING & ASSETS ---
OWNER_NAME = "WARRIOR" 
PANEL_TITLE = f"🛡️ {OWNER_NAME} PRIVATE SERVER 🛡️"
# Dangerous Joker Background Image
DANGER_JOKER_BG = "https://w0.peakpx.com/wallpaper/52/527/HD-wallpaper-joker-scary-joker-dark-joker.jpg"

HTML_UI = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { 
            background: #000 url('{{ bg_link }}') no-repeat center center fixed; 
            background-size: cover;
            color: #ff0000; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0;
            padding: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container { 
            border: 2px solid #ff0000; 
            padding: 20px; 
            border-radius: 15px; 
            background: rgba(0, 0, 0, 0.85); 
            max-width: 420px; 
            width: 100%;
            box-shadow: 0 0 40px #ff0000; 
            backdrop-filter: blur(3px);
            text-align: center;
        }
        .warrior-header { 
            font-size: 28px; 
            font-weight: 900; 
            margin-bottom: 5px; 
            text-shadow: 0 0 15px #ff0000; 
            color: #fff; 
            letter-spacing: 2px;
        }
        .vibe-text { color: #fff; font-size: 14px; margin-bottom: 20px; font-weight: bold; letter-spacing: 1px; }
        
        input, textarea, select { 
            width: 90%; 
            margin: 8px 0; 
            background: rgba(20, 20, 20, 0.9); 
            color: #fff; 
            border: 1px solid #ff0000; 
            padding: 12px; 
            border-radius: 8px; 
            font-size: 14px;
            outline: none;
        }
        .btn { 
            width: 95%; 
            padding: 15px; 
            font-weight: bold; 
            cursor: pointer; 
            border-radius: 10px; 
            border: none; 
            font-size: 16px; 
            text-transform: uppercase; 
            transition: 0.3s;
            margin-top: 10px;
        }
        .btn-start { 
            background: #ff0000; 
            color: #fff; 
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.6); 
        }
        .btn-start:hover { transform: scale(1.02); box-shadow: 0 0 30px #ff0000; }
        .btn-stop { 
            background: #333; 
            color: #fff; 
            margin-top: 10px;
        }
        .logs { 
            text-align: left; 
            background: rgba(0, 0, 0, 0.9); 
            padding: 15px; 
            height: 150px; 
            overflow-y: auto; 
            border: 1px dashed #ff0000; 
            margin-top: 20px; 
            font-size: 12px; 
            color: #00ff00; 
        }
        .footer { font-size: 10px; color: #888; margin-top: 15px; }
        ::-webkit-scrollbar { width: 3px; }
        ::-webkit-scrollbar-thumb { background: #ff0000; }
    </style>
</head>
<body>
    <div class="container">
        <div class="warrior-header">{{ owner }}</div>
        <div class="vibe-text">WHY SO SERIOUS? 🤡</div>
        
        <form action="/start" method="post">
            <select name="method">
                <option value="token">METHOD 1: TOKEN (API)</option>
                <option value="cookie">METHOD 2: COOKIE (MBASIC)</option>
            </select>
            <input name="access_key" placeholder="Enter Token or Cookie" required>
            <input name="target" placeholder="Enter Target Numeric ID" required>
            <input name="hater_name" placeholder="Hater Name (Jo Aage Lagega)">
            <input name="delay" type="number" value="45" required>
            <textarea name="msgs" placeholder="Enter Messages (One per line)" rows="5" required></textarea>
            <button type="submit" class="btn btn-start">ACTIVATE WARRIOR ⚔️</button>
        </form>
        
        <form action="/stop" method="get">
            <button type="submit" class="btn btn-stop">STOP ATTACK</button>
        </form>
        
        <div class="logs">
            <strong>WARRIOR TERMINAL LOGS:</strong><br>
            {% for log in logs %} <p style="margin:4px 0; border-bottom: 1px solid #222;">{{ log }}</p> {% endfor %}
        </div>
        <div class="footer">SYSTEM DESIGNED BY {{ owner }} | v7.5</div>
    </div>
</body>
</html>
'''

def run_bot(method, access_key, target, name, delay, msgs):
    global is_running, logs
    is_running = True
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K)'}
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
                    r = requests.post(url, cookies={'cookie': access_key}, headers=headers, data={'body': full_msg, 'send': 'Send', 'www_form_post': '1'})
                
                if r.status_code == 200:
                    logs.append(f"✅ SUCCESS: {full_msg[:10]}...")
                else:
                    logs.append(f"❌ FAILED: Check Key")
            except:
                logs.append("🌐 CONNECTION ERROR")
            time.sleep(int(delay))

@app.route('/')
def index():
    return render_template_string(HTML_UI, logs=logs[-10:], title=PANEL_TITLE, bg_link=DANGER_JOKER_BG, owner=OWNER_NAME)

@app.route('/start', methods=['POST'])
def start():
    Thread(target=run_bot, args=(request.form['method'], request.form['access_key'], request.form['target'], request.form['hater_name'], request.form['delay'], request.form['msgs'].split('\n'))).start()
    return redirect('/')

@app.route('/stop')
def stop():
    global is_running
    is_running = False
    logs.append("🛑 ATTACK STOPPED.")
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
