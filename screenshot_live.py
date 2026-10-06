from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport
        context = browser.new_context(viewport={'width': 393, 'height': 852}, device_scale_factor=2)
        page = context.new_page()
        print("Navigating to live site...")
        page.goto('https://anhpham94.github.io/percent-demo/3d.html', wait_until='networkidle')
        time.sleep(3)
        page.screenshot(path='live_app_issue.png', full_page=True)
        browser.close()
        print("Done.")

run()
