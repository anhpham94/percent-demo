from playwright.sync_api import sync_playwright

def snap():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
        page.goto("http://localhost:8099/3d.html")
        page.wait_for_timeout(5000)
        browser.close()
snap()
