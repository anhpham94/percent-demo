import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        await page.goto('https://anhpham94.github.io/percent-demo/3d.html')
        await page.wait_for_timeout(4000)
        await page.screenshot(path='live_screenshot.png')
        await browser.close()

asyncio.run(main())
