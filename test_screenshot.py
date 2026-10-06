import sys, asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_viewport_size({"width": 1280, "height": 720})
        await page.goto('http://localhost:8099/3d.html')
        await page.wait_for_timeout(3000)
        await page.screenshot(path='/Users/tuananhpham/work/shopdongho/percent-3d-customizer/screenshot.png')
        await browser.close()

asyncio.run(main())
