import asyncio
from playwright.async_api import async_playwright
import time

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        await page.goto("http://localhost:8099/3d.html")
        
        # Wait for the main studio to load (loading overlay disappears)
        try:
            await page.wait_for_selector('#loading', state='hidden', timeout=15000)
            print("Main studio loaded.")
        except Exception as e:
            print("Timeout waiting for main studio:", e)

        faces = [
            ("none", "Không Mặt"),
            ("apple", "Apple Watch"),
            ("rolex", "Rolex"),
            ("ugia", "Ugia Watch")
        ]
        
        for face_id, face_name in faces:
            print(f"Selecting {face_name}...")
            # Click the watch face option in the UI
            try:
                # the watchface grid cards have an onclick="selectWatchFace('id')"
                await page.evaluate(f"selectWatchFace('{face_id}')")
                
                # Wait for any new loading overlay to hide (when loading watch models)
                # It might appear briefly, wait a little bit
                await asyncio.sleep(0.5)
                await page.wait_for_selector('#loading', state='hidden', timeout=15000)
                
                # Wait for render frame
                await asyncio.sleep(1)
                
                # Take screenshot
                await page.screenshot(path=f"face_{face_id}.png")
                print(f"Screenshot saved for {face_name}")
            except Exception as e:
                print(f"Error selecting {face_name}: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
