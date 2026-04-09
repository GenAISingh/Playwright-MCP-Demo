from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright
from pydantic import BaseModel
import asyncio
import logging
import os
import sys

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Get PORT from environment variable (default to 8000 for Azure App Service)
port = int(os.getenv("PORT", 8000))

mcp = FastMCP(
    "playwright-mcp-server",
    stateless_http=True,
    auth=None,
    host="0.0.0.0"
)

playwright = None
browser = None
context = None
page = None


# Health check endpoint for Azure App Service
@mcp.tool()
async def health_check():
    """Returns OK to satisfy Azure's health probe"""
    logger.info("Health check called")
    return {"status": "healthy"}


# -----------------------------
# Startup Browser (Lazy Loading)
# -----------------------------

async def start_browser():

    global playwright, browser, context, page

    if browser is None:
        logger.info("Initializing Playwright browser...")
        try:
            playwright = await async_playwright().start()
            headless = os.getenv("HEADLESS", "true").lower() != "false"
            browser = await playwright.chromium.launch(
                headless=headless,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            context = await browser.new_context()
            page = await context.new_page()
            logger.info("Browser initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise


# -----------------------------
# Tool: Navigate
# -----------------------------

class NavigateInput(BaseModel):
    url: str


@mcp.tool()
async def browser_navigate(input: NavigateInput):
    await start_browser()
    await page.goto(input.url)

    return {"status": "navigated", "url": input.url}


# -----------------------------
# Tool: Click
# -----------------------------

class ClickInput(BaseModel):
    ref: str


@mcp.tool()
async def browser_click(input: ClickInput):

    await start_browser()
    await page.click(input.ref)

    return {"status": "clicked", "element": input.ref}


# -----------------------------
# Tool: Type
# -----------------------------

class TypeInput(BaseModel):
    ref: str
    text: str


@mcp.tool()
async def browser_type(input: TypeInput):

    await start_browser()
    await page.fill(input.ref, input.text)

    return {"status": "typed", "text": input.text}


# -----------------------------
# Tool: Screenshot
# -----------------------------

class ScreenshotInput(BaseModel):
    filename: str = "screenshot.png"
    fullPage: bool = True


@mcp.tool()
async def browser_take_screenshot(input: ScreenshotInput):

    await start_browser()

    await page.screenshot(
        path=input.filename,
        full_page=input.fullPage
    )

    return {"status": "screenshot_saved", "file": input.filename}


# -----------------------------
# Tool: Evaluate JS
# -----------------------------

class EvaluateInput(BaseModel):
    function: str


@mcp.tool()
async def browser_evaluate(input: EvaluateInput):

    await start_browser()

    result = await page.evaluate(input.function)

    return {"result": result}


# -----------------------------
# Tool: Resize
# -----------------------------

class ResizeInput(BaseModel):
    width: int
    height: int


@mcp.tool()
async def browser_resize(input: ResizeInput):

    await start_browser()

    await page.set_viewport_size({
        "width": input.width,
        "height": input.height
    })

    return {"status": "resized"}


# -----------------------------
# Tool: Close Browser
# -----------------------------

@mcp.tool()
async def browser_close():

    global browser

    if browser:
        await browser.close()
        browser = None

    return {"status": "browser_closed"}


# -----------------------------
# Tool: Snapshot (DOM)
# -----------------------------

@mcp.tool()
async def browser_snapshot():

    await start_browser()

    html = await page.content()

    return {"html": html}


# -----------------------------
# Tool: Press Key
# -----------------------------

class KeyInput(BaseModel):
    key: str


@mcp.tool()
async def browser_press_key(input: KeyInput):

    await start_browser()

    await page.keyboard.press(input.key)

    return {"status": "key_pressed"}


# -----------------------------
# Run Server
# -----------------------------

if __name__ == "__main__":
    try:
        logger.info(f"Starting Playwright MCP server on 0.0.0.0:{port}")
        sys.stdout.flush()
        
        # Run with streamable HTTP transport
        # FastMCP will use PORT environment variable if set, otherwise defaults to 8000
        mcp.run(transport="streamable-http")
        
    except Exception as e:
        logger.error(f"Error starting server: {e}", exc_info=True)
        sys.exit(1)