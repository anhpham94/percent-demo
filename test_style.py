from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 393, 'height': 852})
        page = context.new_page()
        page.goto('http://localhost:8099/3d.html', wait_until='networkidle')
        pos = page.evaluate("window.getComputedStyle(document.querySelector('.config-footer')).position")
        print(f"Footer position: {pos}")
        browser.close()

run()
