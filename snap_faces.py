from playwright.sync_api import sync_playwright
import time

def snap():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8099/test_faces.html")
        page.wait_for_selector("#loading", state="hidden")
        
        # Snap Rolex
        page.select_option("#faceSelect", "rolex")
        page.click("button")
        time.sleep(1)
        page.wait_for_selector("#loading", state="hidden", timeout=10000)
        page.screenshot(path="face_rolex.png")
        
        # Snap Apple
        page.select_option("#faceSelect", "apple")
        page.click("button")
        time.sleep(1)
        page.wait_for_selector("#loading", state="hidden", timeout=20000)
        page.screenshot(path="face_apple.png")
        
        # Snap Smart
        page.select_option("#faceSelect", "smart")
        page.click("button")
        time.sleep(1)
        page.wait_for_selector("#loading", state="hidden", timeout=10000)
        page.screenshot(path="face_smart.png")

        browser.close()

snap()
