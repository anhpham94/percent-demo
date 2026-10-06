from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("console", lambda msg: print(f"CONSOLE: {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"ERROR: {err}"))
        print("Navigating...")
        page.goto('https://anhpham94.github.io/percent-demo/3d.html', wait_until='networkidle')
        time.sleep(3)
        page.screenshot(path='error_screenshot.png')
        browser.close()

run()
