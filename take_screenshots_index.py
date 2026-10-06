import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        await page.goto('http://localhost:8099/index.html')
        await page.wait_for_timeout(3000)
        
        await page.click('text=Chronograph')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='index_screenshot_chrono.png')
        await browser.close()

asyncio.run(main())
