import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on("console", lambda msg: print(f"Console {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"Page Error: {err}"))
        
        print("Navigating to 3d.html...")
        await page.goto('https://anhpham94.github.io/percent-demo/3d.html')
        await page.wait_for_timeout(3000)
        
        print("Page loaded. Checking for models...")
        
        await browser.close()

asyncio.run(main())
