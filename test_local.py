from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 393, 'height': 852}, device_scale_factor=2)
        page = context.new_page()
        
        print("Navigating to local 3d.html...")
        page.goto('http://localhost:8099/3d.html')
        time.sleep(3) # wait for models
        
        # Test interacting with watch face
        print("Clicking Apple Watch face...")
        page.evaluate("setWatchFace('smart_apple', document.querySelectorAll('.watchface-pill')[1])")
        time.sleep(1)
        
        # Click on second leather (Karl Sepia)
        print("Clicking second leather option...")
        # Get the second leather option by evaluating
        page.evaluate("document.querySelectorAll('.leather-card')[1].click()")
        time.sleep(1)
        
        # Click on deployant buckle
        print("Clicking deployant buckle...")
        page.evaluate("document.querySelectorAll('.size-pill')[1].click()") # The second pill in buckle size group is deployant
        time.sleep(1)
        
        # Check if price updated
        price = page.evaluate("document.getElementById('total-price-footer').innerText")
        print(f"Price updated to: {price}")
        
        print("Final state screenshot...")
        page.screenshot(path='test_final_local.png')
        browser.close()

run()
