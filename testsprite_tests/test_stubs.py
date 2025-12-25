"""
Test Stubs Module
Contains stub functions for common Playwright test operations
"""
import asyncio
from playwright import async_api
from playwright.async_api import Page, Browser, BrowserContext, Playwright
from typing import Optional, List, Dict, Any


async def stub_playwright_start() -> Playwright:
    """
    Stub: Initialize and start Playwright session
    Returns: Playwright instance
    """
    pw = await async_api.async_playwright().start()
    return pw


async def stub_launch_browser(
    pw: Playwright,
    headless: bool = True,
    window_size: str = "1280,720"
) -> Browser:
    """
    Stub: Launch a Chromium browser with standard arguments

    Args:
        pw: Playwright instance
        headless: Run browser in headless mode
        window_size: Browser window dimensions

    Returns: Browser instance
    """
    browser = await pw.chromium.launch(
        headless=headless,
        args=[
            f"--window-size={window_size}",
            "--disable-dev-shm-usage",
            "--ipc=host",
            "--single-process"
        ],
    )
    return browser


async def stub_create_context(
    browser: Browser,
    default_timeout: int = 5000
) -> BrowserContext:
    """
    Stub: Create a new browser context with default timeout

    Args:
        browser: Browser instance
        default_timeout: Default timeout in milliseconds

    Returns: BrowserContext instance
    """
    context = await browser.new_context()
    context.set_default_timeout(default_timeout)
    return context


async def stub_create_page(context: BrowserContext) -> Page:
    """
    Stub: Open a new page in the browser context

    Args:
        context: BrowserContext instance

    Returns: Page instance
    """
    page = await context.new_page()
    return page


async def stub_navigate_to_url(
    page: Page,
    url: str,
    wait_until: str = "commit",
    timeout: int = 10000
) -> None:
    """
    Stub: Navigate to a URL with specified wait condition

    Args:
        page: Page instance
        url: Target URL
        wait_until: Wait condition (commit, load, domcontentloaded, networkidle)
        timeout: Navigation timeout in milliseconds
    """
    await page.goto(url, wait_until=wait_until, timeout=timeout)


async def stub_wait_for_load_state(
    page: Page,
    state: str = "domcontentloaded",
    timeout: int = 3000
) -> None:
    """
    Stub: Wait for page to reach a specific load state

    Args:
        page: Page instance
        state: Load state to wait for
        timeout: Wait timeout in milliseconds
    """
    try:
        await page.wait_for_load_state(state, timeout=timeout)
    except async_api.Error:
        pass


async def stub_wait_for_all_frames(
    page: Page,
    state: str = "domcontentloaded",
    timeout: int = 3000
) -> None:
    """
    Stub: Wait for all iframes to load

    Args:
        page: Page instance
        state: Load state to wait for
        timeout: Wait timeout in milliseconds
    """
    for frame in page.frames:
        try:
            await frame.wait_for_load_state(state, timeout=timeout)
        except async_api.Error:
            pass


async def stub_full_page_setup(
    url: str = "http://localhost:3000",
    headless: bool = True,
    default_timeout: int = 5000
) -> tuple[Playwright, Browser, BrowserContext, Page]:
    """
    Stub: Complete page setup with all initialization steps

    Args:
        url: Target URL to navigate to
        headless: Run browser in headless mode
        default_timeout: Default timeout in milliseconds

    Returns: Tuple of (Playwright, Browser, BrowserContext, Page)
    """
    pw = await stub_playwright_start()
    browser = await stub_launch_browser(pw, headless=headless)
    context = await stub_create_context(browser, default_timeout=default_timeout)
    page = await stub_create_page(context)

    await stub_navigate_to_url(page, url)
    await stub_wait_for_load_state(page)
    await stub_wait_for_all_frames(page)

    return pw, browser, context, page


async def stub_cleanup(
    context: Optional[BrowserContext] = None,
    browser: Optional[Browser] = None,
    pw: Optional[Playwright] = None
) -> None:
    """
    Stub: Clean up browser resources

    Args:
        context: BrowserContext to close
        browser: Browser to close
        pw: Playwright instance to stop
    """
    if context:
        await context.close()
    if browser:
        await browser.close()
    if pw:
        await pw.stop()


async def stub_click_element(
    page: Page,
    selector: str,
    timeout: int = 5000
) -> None:
    """
    Stub: Click an element with retry logic

    Args:
        page: Page instance
        selector: Element selector
        timeout: Click timeout in milliseconds
    """
    await page.click(selector, timeout=timeout)


async def stub_fill_input(
    page: Page,
    selector: str,
    value: str,
    timeout: int = 5000
) -> None:
    """
    Stub: Fill an input field

    Args:
        page: Page instance
        selector: Input selector
        value: Value to fill
        timeout: Fill timeout in milliseconds
    """
    await page.fill(selector, value, timeout=timeout)


async def stub_select_option(
    page: Page,
    selector: str,
    value: str,
    timeout: int = 5000
) -> None:
    """
    Stub: Select an option from a dropdown

    Args:
        page: Page instance
        selector: Select element selector
        value: Option value to select
        timeout: Select timeout in milliseconds
    """
    await page.select_option(selector, value, timeout=timeout)


async def stub_wait_for_selector(
    page: Page,
    selector: str,
    state: str = "visible",
    timeout: int = 30000
) -> None:
    """
    Stub: Wait for an element to reach a specific state

    Args:
        page: Page instance
        selector: Element selector
        state: State to wait for (visible, hidden, attached, detached)
        timeout: Wait timeout in milliseconds
    """
    await page.wait_for_selector(selector, state=state, timeout=timeout)


async def stub_get_text(
    page: Page,
    selector: str
) -> str:
    """
    Stub: Get text content of an element

    Args:
        page: Page instance
        selector: Element selector

    Returns: Text content
    """
    return await page.text_content(selector)


async def stub_take_screenshot(
    page: Page,
    path: str,
    full_page: bool = True
) -> None:
    """
    Stub: Take a screenshot of the page

    Args:
        page: Page instance
        path: Screenshot file path
        full_page: Capture full page or viewport only
    """
    await page.screenshot(path=path, full_page=full_page)


async def stub_intercept_route(
    page: Page,
    url_pattern: str,
    handler: Any
) -> None:
    """
    Stub: Intercept network requests matching a pattern

    Args:
        page: Page instance
        url_pattern: URL pattern to intercept
        handler: Route handler function
    """
    await page.route(url_pattern, handler)


async def stub_wait_for_network_idle(
    page: Page,
    timeout: int = 30000
) -> None:
    """
    Stub: Wait for network to become idle

    Args:
        page: Page instance
        timeout: Wait timeout in milliseconds
    """
    await page.wait_for_load_state("networkidle", timeout=timeout)


async def stub_execute_script(
    page: Page,
    script: str
) -> Any:
    """
    Stub: Execute JavaScript in the page context

    Args:
        page: Page instance
        script: JavaScript code to execute

    Returns: Script execution result
    """
    return await page.evaluate(script)


async def stub_get_cookies(
    context: BrowserContext
) -> List[Dict[str, Any]]:
    """
    Stub: Get all cookies from the browser context

    Args:
        context: BrowserContext instance

    Returns: List of cookies
    """
    return await context.cookies()


async def stub_set_cookies(
    context: BrowserContext,
    cookies: List[Dict[str, Any]]
) -> None:
    """
    Stub: Set cookies in the browser context

    Args:
        context: BrowserContext instance
        cookies: List of cookies to set
    """
    await context.add_cookies(cookies)


async def stub_clear_cookies(
    context: BrowserContext
) -> None:
    """
    Stub: Clear all cookies from the browser context

    Args:
        context: BrowserContext instance
    """
    await context.clear_cookies()


def stub_sleep(seconds: float) -> None:
    """
    Stub: Sleep for a specified duration (synchronous)

    Args:
        seconds: Sleep duration in seconds
    """
    import time
    time.sleep(seconds)


async def stub_async_sleep(seconds: float) -> None:
    """
    Stub: Async sleep for a specified duration

    Args:
        seconds: Sleep duration in seconds
    """
    await asyncio.sleep(seconds)
