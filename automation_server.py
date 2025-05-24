from flask import Flask, request, jsonify
from threading import Thread
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import queue

app = Flask(__name__)
cmd_queue = queue.Queue()
log_queue = queue.Queue()

def log(msg):
    print(msg)
    log_queue.put(msg)

def automation_worker(page):
    youtube_open = False
    while True:
        cmd = cmd_queue.get()
        action = cmd.get('action')
        item = cmd.get('item')
        log(f"[Automation] Received command: {cmd}")
        if action == 'play':
            if not youtube_open:
                page.goto("https://www.youtube.com")
                youtube_open = True
            try:
                page.wait_for_selector("input#search", timeout=15000)
                page.fill("input#search", item)
                page.keyboard.press("Enter")
                page.wait_for_selector("ytd-video-renderer a#video-title", timeout=15000)
                first_video = page.query_selector("ytd-video-renderer a#video-title")
                if first_video:
                    first_video.click()
                    log(f"[Automation] Playing: {item}")
                else:
                    log("[Automation] No video results found.")
            except Exception as e:
                log(f"[Automation] Error: {e}")
        elif action == 'next':
            try:
                page.keyboard.press('Shift+N')
                log("[Automation] Pressed Next (Shift+N)")
            except Exception as e:
                log(f"[Automation] Error pressing Next: {e}")
        elif action == 'pause':
            try:
                page.keyboard.press('k')
                log("[Automation] Toggled Pause/Play (k)")
            except Exception as e:
                log(f"[Automation] Error pressing Pause: {e}")
        cmd_queue.task_done()

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    cmd_queue.put(data)
    return jsonify({'status': 'received'})

@app.route('/logs')
def logs():
    logs = []
    while not log_queue.empty():
        logs.append(log_queue.get())
    return jsonify({'logs': logs})

if __name__ == '__main__':
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    Thread(target=automation_worker, args=(page,), daemon=True).start()
    app.run(port=5051, debug=False, use_reloader=False) 