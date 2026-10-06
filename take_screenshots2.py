import asyncio
from playwright.async_api import async_playwright
import time

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        await page.goto("http://localhost:8099/3d.html")
        await page.wait_for_selector('#loading', state='hidden', timeout=15000)

        faces = ["none", "apple", "rolex", "ugia"]
        
        for face_id in faces:
            await page.evaluate(f"selectWatchFace('{face_id}')")
            await asyncio.sleep(2) # Give it 2 seconds to load and render
            await page.screenshot(path=f"face_{face_id}_2.png")
            print(f"Screenshot saved for {face_id}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
