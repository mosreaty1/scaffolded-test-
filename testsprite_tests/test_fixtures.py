"""
Test Fixtures Module
Contains pytest fixtures for common test setup and teardown
"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from playwright.async_api import (
    Playwright,
    Browser,
    BrowserContext,
    Page,
    async_playwright
)
from test_stubs import (
    stub_playwright_start,
    stub_launch_browser,
    stub_create_context,
    stub_create_page,
    stub_cleanup,
    stub_navigate_to_url,
    stub_wait_for_load_state,
    stub_wait_for_all_frames
)
from test_mocks import (
    mock_user_data,
    mock_product_data,
    mock_order_data,
    mock_cart_data,
    mock_authentication_success
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Fixture: Create an event loop for the test session

    Yields: Event loop
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def playwright_instance() -> AsyncGenerator[Playwright, None]:
    """
    Fixture: Initialize Playwright for the test session

    Yields: Playwright instance
    """
    pw = await stub_playwright_start()
    yield pw
    await pw.stop()


@pytest.fixture(scope="session")
async def browser(playwright_instance: Playwright) -> AsyncGenerator[Browser, None]:
    """
    Fixture: Launch browser for the test session

    Args:
        playwright_instance: Playwright instance

    Yields: Browser instance
    """
    browser = await stub_launch_browser(playwright_instance)
    yield browser
    await browser.close()


@pytest.fixture
async def context(browser: Browser) -> AsyncGenerator[BrowserContext, None]:
    """
    Fixture: Create a new browser context for each test

    Args:
        browser: Browser instance

    Yields: BrowserContext instance
    """
    context = await stub_create_context(browser)
    yield context
    await context.close()


@pytest.fixture
async def page(context: BrowserContext) -> AsyncGenerator[Page, None]:
    """
    Fixture: Create a new page for each test

    Args:
        context: BrowserContext instance

    Yields: Page instance
    """
    page = await stub_create_page(context)
    yield page
    await page.close()


@pytest.fixture
async def authenticated_page(
    context: BrowserContext
) -> AsyncGenerator[Page, None]:
    """
    Fixture: Create a new page with authentication cookies

    Args:
        context: BrowserContext instance

    Yields: Authenticated Page instance
    """
    auth_data = mock_authentication_success()
    await context.add_cookies([
        {
            "name": "auth_token",
            "value": auth_data["token"],
            "domain": "localhost",
            "path": "/"
        }
    ])
    page = await stub_create_page(context)
    yield page
    await page.close()


@pytest.fixture
async def page_with_url(
    page: Page,
    request
) -> AsyncGenerator[Page, None]:
    """
    Fixture: Create a page and navigate to a specific URL

    Args:
        page: Page instance
        request: Pytest request object with param containing URL

    Yields: Page instance navigated to URL
    """
    url = getattr(request, 'param', 'http://localhost:3000')
    await stub_navigate_to_url(page, url)
    await stub_wait_for_load_state(page)
    await stub_wait_for_all_frames(page)
    yield page


@pytest.fixture
def mock_user():
    """
    Fixture: Generate mock user data

    Returns: Mock user dictionary
    """
    return mock_user_data()


@pytest.fixture
def mock_customer():
    """
    Fixture: Generate mock customer user data

    Returns: Mock customer dictionary
    """
    return mock_user_data(role="customer")


@pytest.fixture
def mock_vendor():
    """
    Fixture: Generate mock vendor user data

    Returns: Mock vendor dictionary
    """
    return mock_user_data(role="vendor")


@pytest.fixture
def mock_admin():
    """
    Fixture: Generate mock admin user data

    Returns: Mock admin dictionary
    """
    return mock_user_data(role="admin")


@pytest.fixture
def mock_product():
    """
    Fixture: Generate mock product data

    Returns: Mock product dictionary
    """
    return mock_product_data()


@pytest.fixture
def mock_products():
    """
    Fixture: Generate multiple mock products

    Returns: List of mock product dictionaries
    """
    return [mock_product_data() for _ in range(5)]


@pytest.fixture
def mock_order():
    """
    Fixture: Generate mock order data

    Returns: Mock order dictionary
    """
    return mock_order_data()


@pytest.fixture
def mock_cart():
    """
    Fixture: Generate mock shopping cart data

    Returns: Mock cart dictionary
    """
    return mock_cart_data()


@pytest.fixture
def mock_auth_token():
    """
    Fixture: Generate mock authentication token

    Returns: Mock authentication response
    """
    return mock_authentication_success()


@pytest.fixture
async def intercepted_page(page: Page) -> AsyncGenerator[Page, None]:
    """
    Fixture: Create a page with network interception enabled

    Args:
        page: Page instance

    Yields: Page with route interception
    """
    intercepted_routes = []

    async def default_handler(route):
        intercepted_routes.append(route.request.url)
        await route.continue_()

    await page.route("**/*", default_handler)
    yield page
    intercepted_routes.clear()


@pytest.fixture
def base_url():
    """
    Fixture: Provide base URL for tests

    Returns: Base URL string
    """
    return "http://localhost:3000"


@pytest.fixture
def api_base_url():
    """
    Fixture: Provide API base URL for tests

    Returns: API base URL string
    """
    return "http://localhost:3000/api"


@pytest.fixture
def test_credentials():
    """
    Fixture: Provide test user credentials

    Returns: Dictionary with test credentials
    """
    return {
        "customer": {
            "email": "customer@test.com",
            "password": "Test123456!"
        },
        "vendor": {
            "email": "vendor@test.com",
            "password": "Test123456!"
        },
        "admin": {
            "email": "admin@test.com",
            "password": "Admin123456!"
        }
    }


@pytest.fixture
async def screenshot_on_failure(page: Page, request):
    """
    Fixture: Take screenshot on test failure

    Args:
        page: Page instance
        request: Pytest request object
    """
    yield
    if request.node.rep_call.failed:
        screenshot_path = f"screenshots/{request.node.name}.png"
        await page.screenshot(path=screenshot_path, full_page=True)


@pytest.fixture
def performance_tracker():
    """
    Fixture: Track performance metrics during tests

    Returns: Performance tracking dictionary
    """
    metrics = {
        "start_time": None,
        "end_time": None,
        "duration": None,
        "events": []
    }

    def start():
        import time
        metrics["start_time"] = time.time()

    def stop():
        import time
        metrics["end_time"] = time.time()
        if metrics["start_time"]:
            metrics["duration"] = metrics["end_time"] - metrics["start_time"]

    def add_event(name: str):
        import time
        metrics["events"].append({
            "name": name,
            "timestamp": time.time()
        })

    metrics["start"] = start
    metrics["stop"] = stop
    metrics["add_event"] = add_event

    return metrics


@pytest.fixture
async def mobile_page(context: BrowserContext) -> AsyncGenerator[Page, None]:
    """
    Fixture: Create a page with mobile viewport

    Args:
        context: BrowserContext instance

    Yields: Page with mobile viewport
    """
    await context.set_viewport_size({"width": 375, "height": 667})
    page = await stub_create_page(context)
    yield page
    await page.close()


@pytest.fixture
async def tablet_page(context: BrowserContext) -> AsyncGenerator[Page, None]:
    """
    Fixture: Create a page with tablet viewport

    Args:
        context: BrowserContext instance

    Yields: Page with tablet viewport
    """
    await context.set_viewport_size({"width": 768, "height": 1024})
    page = await stub_create_page(context)
    yield page
    await page.close()


@pytest.fixture
async def slow_network_page(context: BrowserContext) -> AsyncGenerator[Page, None]:
    """
    Fixture: Create a page with simulated slow network

    Args:
        context: BrowserContext instance

    Yields: Page with network throttling
    """
    await context.route("**/*", lambda route: route.continue_(
        timeout=5000
    ))
    page = await stub_create_page(context)
    yield page
    await page.close()


@pytest.fixture(autouse=True)
async def cleanup_after_test():
    """
    Fixture: Automatic cleanup after each test

    Yields: None
    """
    yield
    # Cleanup code can be added here


@pytest.fixture
def test_data_factory():
    """
    Fixture: Factory for generating various test data

    Returns: Dictionary of factory functions
    """
    return {
        "user": mock_user_data,
        "product": mock_product_data,
        "order": mock_order_data,
        "cart": mock_cart_data
    }


@pytest.fixture
async def console_logger(page: Page):
    """
    Fixture: Capture console messages during tests

    Args:
        page: Page instance

    Returns: List of console messages
    """
    messages = []

    def handle_console(msg):
        messages.append({
            "type": msg.type,
            "text": msg.text,
            "location": msg.location
        })

    page.on("console", handle_console)
    yield messages
    page.remove_listener("console", handle_console)


@pytest.fixture
async def network_logger(page: Page):
    """
    Fixture: Capture network requests during tests

    Args:
        page: Page instance

    Returns: List of network requests
    """
    requests = []

    def handle_request(request):
        requests.append({
            "url": request.url,
            "method": request.method,
            "headers": request.headers,
            "resource_type": request.resource_type
        })

    page.on("request", handle_request)
    yield requests
    page.remove_listener("request", handle_request)


@pytest.fixture
def test_timeout():
    """
    Fixture: Provide standard test timeouts

    Returns: Dictionary of timeout values
    """
    return {
        "short": 3000,
        "medium": 10000,
        "long": 30000,
        "navigation": 10000,
        "assertion": 30000
    }
