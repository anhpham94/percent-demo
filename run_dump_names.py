import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://localhost:8099/dump_mesh_names.html')
        await page.wait_for_timeout(3000)
        print(await page.locator('#res').inner_text())
        await browser.close()
asyncio.run(main())
