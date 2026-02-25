from patchright.async_api import async_playwright

playwright = None
browser = None

BROWSER_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
]

async def start_browser():
    global playwright, browser
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=True,
        args=BROWSER_ARGS
    )
    print("Browser started")

async def stop_browser():
    await browser.close()
    await playwright.stop()
    print("Browser stopped")

def get_browser():
    return browser