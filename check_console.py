import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        page.on("console", lambda msg: print(f"Console {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"Page Error: {err}"))
        
        await page.goto('http://localhost:8099/index.html')
        await page.wait_for_timeout(2000)
        
        # Click on Apple Watch
        try:
            await page.click('text=Apple')
        except Exception as e:
            print("Could not click Apple:", e)
        await page.wait_for_timeout(1000)
        
        # Click on a leather option
        try:
            await page.click('text=Nâu đất Soil')
        except Exception as e:
            print("Could not click Leather:", e)
            
        await page.wait_for_timeout(1000)
        await browser.close()

asyncio.run(main())
