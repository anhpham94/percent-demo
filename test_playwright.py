import sys, json, time, asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('http://localhost:8099/test_glb.html')
        await page.wait_for_timeout(3000)
        info = await page.locator('#info').inner_text()
        print(info)
        await page.screenshot(path='/Users/tuananhpham/work/shopdongho/percent-3d-customizer/test_glb.png')
        await browser.close()

asyncio.run(main())
