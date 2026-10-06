from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport (iPhone 14 Pro)
        context = browser.new_context(viewport={'width': 393, 'height': 852}, device_scale_factor=2)
        page = context.new_page()
        page.goto('http://localhost:8099/index.html')
        time.sleep(3) # Wait for three.js and images to load
        page.screenshot(path='mobile_view.png', full_page=False)
        browser.close()

run()
