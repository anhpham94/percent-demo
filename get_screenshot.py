import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        await page.goto('http://localhost:8099/index.html')
        await page.wait_for_timeout(4000)
        
        await page.screenshot(path='/Users/tuananhpham/.gemini/antigravity-ide/brain/9213cad5-45b6-4ad8-a01b-4828b2c38f34/fixed_app.png')
        
        await browser.close()
asyncio.run(main())
