from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import shutil
import os
import time
import sys

# Detect if running in a cloud/headless environment
IS_CLOUD = bool(os.environ.get("RENDER")) or (sys.platform != "win32" and not os.environ.get("DISPLAY"))

def get_chrome_path():
    possible_paths = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    chrome_path = shutil.which("chrome")
    if chrome_path:
        return chrome_path
    raise FileNotFoundError("Google Chrome executable not found on this system.")

# Initialize Playwright and browser globally
if not IS_CLOUD:
    playwright = sync_playwright().start()
    chrome_path = get_chrome_path()
    browser = playwright.chromium.launch(headless=False, executable_path=chrome_path)
else:
    playwright = None
    chrome_path = None
    browser = None

# Keep track of the last YouTube page
last_youtube_page = None

def execute_plan(plan: dict):
    if IS_CLOUD:
        print("[Automation] Browser automation is not supported in this environment. Please run locally for full functionality.")
        return
    site = plan.get("site", "Unknown").lower()
    action = plan.get("action", "Unknown").lower()
    item = plan.get("item", "")
    filters = plan.get("filters", {})

    if site == "youtube":
        if action == "play":
            youtube_search_and_play(item)
        elif action == "next":
            youtube_next()
        elif action == "previous":
            youtube_previous()
        else:
            print(f"[Automation] Action '{action}' not supported for YouTube.")
    else:
        print(f"[Automation] Site '{site}' not supported yet.")

def youtube_search_and_play(video_title):
    global last_youtube_page
    if last_youtube_page and not last_youtube_page.is_closed():
        page = last_youtube_page
        page.bring_to_front()
        page.goto("https://www.youtube.com")
    else:
        page = browser.new_page()
        last_youtube_page = page
        page.goto("https://www.youtube.com")
    print("[Automation] Navigating to YouTube...")
    try:
        consent_selectors = [
            'button:has-text("Accept all")',
            'button:has-text("I agree")',
            'button:has-text("AGREE")',
            'button:has-text("Accept")',
            'button:has-text("Yes, I agree")'
        ]
        for selector in consent_selectors:
            try:
                page.click(selector, timeout=3000)
                print(f"[Automation] Clicked consent button: {selector}")
                break
            except Exception:
                continue
        print(f"[Automation] Searching for video: {video_title}")
        try:
            page.wait_for_selector("input#search", timeout=15000)
            page.fill("input#search", video_title)
        except PlaywrightTimeoutError:
            try:
                page.wait_for_selector("input[name='search_query']", timeout=5000)
                page.fill("input[name='search_query']", video_title)
            except Exception:
                print("[Automation] Could not find any search box.")
                page.screenshot(path='youtube_error.png')
                print("[Automation] Screenshot saved as youtube_error.png")
                return
        page.keyboard.press("Enter")
        page.wait_for_selector("ytd-video-renderer a#video-title", timeout=15000)
        first_video = page.query_selector("ytd-video-renderer a#video-title")
        if first_video:
            first_video.click()
            print("[Automation] Playing first video result.")
        else:
            print("[Automation] No video results found.")
    except PlaywrightTimeoutError:
        print("[Automation] YouTube search box or results not found (timeout).")
        page.screenshot(path='youtube_error.png')
        print("[Automation] Screenshot saved as youtube_error.png")
    except Exception as e:
        print(f"[Automation] Error handling YouTube results: {e}")
        page.screenshot(path='youtube_error.png')
        print("[Automation] Screenshot saved as youtube_error.png")
    print("[Automation] Browser will remain open. Please close it manually when done.")

def youtube_next():
    global last_youtube_page
    if last_youtube_page:
        try:
            last_youtube_page.keyboard.press('Shift+N')
            print("[Automation] Pressed Next (Shift+N) on YouTube.")
        except Exception as e:
            print(f"[Automation] Error pressing Next: {e}")
    else:
        print("[Automation] No YouTube page available for Next action.")

def youtube_previous():
    global last_youtube_page
    if last_youtube_page:
        try:
            last_youtube_page.keyboard.press('Shift+P')
            print("[Automation] Pressed Previous (Shift+P) on YouTube.")
        except Exception as e:
            print(f"[Automation] Error pressing Previous: {e}")
    else:
        print("[Automation] No YouTube page available for Previous action.") 