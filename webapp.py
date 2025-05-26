from flask import Flask, render_template, request, jsonify, session
import queue
import subprocess
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session
log_queue = queue.Queue()

# Thread-safe log function
def log(msg):
    log_queue.put(msg)

# Patch automation to use our log
import builtins
builtins.print = log

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    command = request.form['command']
    # Update chat history in session
    if 'history' not in session:
        session['history'] = []
    session['history'].append({'role': 'user', 'content': command})
    session.modified = True
    log("[Debug] Running automation subprocess...")
    # Call run_automation.py as a subprocess, passing history as JSON
    history_json = json.dumps(session['history'])
    result = subprocess.run(
        ['python', 'run_automation.py', command, history_json],
        capture_output=True, text=True
    )
    log(f"[Debug] Subprocess finished with return code: {result.returncode}")
    log(f"[Debug] STDOUT: {result.stdout}")
    log(f"[Debug] STDERR: {result.stderr}")
    if result.stdout:
        for line in result.stdout.splitlines():
            log(line)
    if result.stderr:
        for line in result.stderr.splitlines():
            log(f"[Error] {line}")
    return jsonify({'status': 'done'})

@app.route('/logs')
def logs():
    logs = []
    while not log_queue.empty():
        logs.append(log_queue.get())
    return jsonify({'logs': logs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True) 