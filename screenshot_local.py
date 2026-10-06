import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto('http://localhost:8099/index.html')
        await page.wait_for_timeout(3000)
        
        # Snapshot full page
        await page.screenshot(path='current_local_state.png', full_page=True)
        
        await browser.close()

asyncio.run(main())
