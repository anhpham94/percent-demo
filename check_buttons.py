import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        page.on("console", lambda msg: print(f"Console {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"Page Error: {err}"))
        
        await page.goto('https://anhpham94.github.io/percent-demo/3d.html')
        await page.wait_for_timeout(2000)
        
        print("Clicking a leather button...")
        try:
            await page.click('button:has-text("Nâu Đậm (Epsom)")')
            await page.wait_for_timeout(1000)
            
            await page.click('#btn-toggle-rotate')
            await page.wait_for_timeout(1000)
        except Exception as e:
            print("Exception clicking buttons:", e)
        
        await browser.close()

asyncio.run(main())
