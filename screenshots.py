import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        await page.goto('https://anhpham94.github.io/percent-demo/3d.html')
        await page.wait_for_timeout(3000)
        
        # Take default screenshot
        await page.screenshot(path='ui_screenshot_default.png')
        
        # Click a different leather card
        try:
            # First leather card is usually active, click the second one
            await page.click('.leather-card:nth-child(2)')
            await page.wait_for_timeout(1000)
            await page.screenshot(path='ui_screenshot_leather_changed.png')
            
            # Click checkout button
            await page.click('button:has-text("🛒 HOÀN TẤT & ĐẶT MAY")')
            await page.wait_for_timeout(1000)
            await page.screenshot(path='ui_screenshot_checkout_modal.png')
        except Exception as e:
            print("Error interacting:", e)
            
        await browser.close()

asyncio.run(main())
