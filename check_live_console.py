from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        errors = []
        page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))
        page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == 'error' else None)
        
        print("Navigating to live site...")
        page.goto('https://anhpham94.github.io/percent-demo/3d.html', wait_until='networkidle')
        
        if errors:
            print("ERRORS FOUND:")
            for e in errors:
                print(e)
        else:
            print("NO CONSOLE ERRORS.")
            
        browser.close()

run()
