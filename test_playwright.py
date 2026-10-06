import sys, json, time, asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.on("console", lambda msg: print(f"Console: {msg.text}"))
        page.on("pageerror", lambda err: print(f"PageError: {err}"))
        await page.goto('http://localhost:8099/3d.html')
        await page.wait_for_timeout(3000)
        await browser.close()

asyncio.run(main())
