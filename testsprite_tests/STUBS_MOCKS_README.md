# Test Stubs and Mocks Documentation

This documentation covers the comprehensive stub and mock functions available for testing.

## Table of Contents

1. [Overview](#overview)
2. [Stub Functions](#stub-functions)
3. [Mock Functions](#mock-functions)
4. [Fixtures](#fixtures)
5. [Usage Examples](#usage-examples)
6. [Best Practices](#best-practices)

---

## Overview

This testing framework provides three main modules:

- **test_stubs.py** - Reusable stub functions for common Playwright operations
- **test_mocks.py** - Mock functions for external dependencies and test data
- **test_fixtures.py** - Pytest fixtures for easy test setup and teardown
- **conftest.py** - Pytest configuration to auto-load fixtures

---

## Stub Functions

### Browser Setup Stubs

#### `stub_playwright_start()`
Initialize and start Playwright session.

```python
pw = await stub_playwright_start()
```

#### `stub_launch_browser(pw, headless=True, window_size="1280,720")`
Launch a Chromium browser with standard arguments.

```python
browser = await stub_launch_browser(pw, headless=True)
```

#### `stub_create_context(browser, default_timeout=5000)`
Create a new browser context with default timeout.

```python
context = await stub_create_context(browser, default_timeout=5000)
```

#### `stub_create_page(context)`
Open a new page in the browser context.

```python
page = await stub_create_page(context)
```

#### `stub_full_page_setup(url="http://localhost:3000", headless=True, default_timeout=5000)`
Complete page setup with all initialization steps in one call.

```python
pw, browser, context, page = await stub_full_page_setup(
    url="http://localhost:3000",
    headless=True
)
```

### Navigation Stubs

#### `stub_navigate_to_url(page, url, wait_until="commit", timeout=10000)`
Navigate to a URL with specified wait condition.

```python
await stub_navigate_to_url(page, "http://localhost:3000/login")
```

#### `stub_wait_for_load_state(page, state="domcontentloaded", timeout=3000)`
Wait for page to reach a specific load state.

```python
await stub_wait_for_load_state(page, "networkidle")
```

#### `stub_wait_for_all_frames(page, state="domcontentloaded", timeout=3000)`
Wait for all iframes to load.

```python
await stub_wait_for_all_frames(page)
```

### Interaction Stubs

#### `stub_click_element(page, selector, timeout=5000)`
Click an element with retry logic.

```python
await stub_click_element(page, "button#submit")
```

#### `stub_fill_input(page, selector, value, timeout=5000)`
Fill an input field.

```python
await stub_fill_input(page, "#email", "test@example.com")
```

#### `stub_select_option(page, selector, value, timeout=5000)`
Select an option from a dropdown.

```python
await stub_select_option(page, "#country", "USA")
```

#### `stub_wait_for_selector(page, selector, state="visible", timeout=30000)`
Wait for an element to reach a specific state.

```python
await stub_wait_for_selector(page, "text=Success", state="visible")
```

### Utility Stubs

#### `stub_get_text(page, selector)`
Get text content of an element.

```python
text = await stub_get_text(page, ".message")
```

#### `stub_take_screenshot(page, path, full_page=True)`
Take a screenshot of the page.

```python
await stub_take_screenshot(page, "screenshots/error.png")
```

#### `stub_execute_script(page, script)`
Execute JavaScript in the page context.

```python
result = await stub_execute_script(page, "return document.title")
```

#### `stub_async_sleep(seconds)`
Async sleep for a specified duration.

```python
await stub_async_sleep(2)  # Sleep for 2 seconds
```

### Cleanup Stubs

#### `stub_cleanup(context=None, browser=None, pw=None)`
Clean up browser resources.

```python
await stub_cleanup(context, browser, pw)
```

---

## Mock Functions

### Mock Data Generators

#### `mock_user_data(user_id=None, email=None, role="customer")`
Generate mock user data.

```python
user = mock_user_data(email="test@example.com", role="vendor")
# Returns: {id, email, username, role, first_name, last_name, ...}
```

#### `mock_product_data(product_id=None, vendor_id=None, stock=100)`
Generate mock product data.

```python
product = mock_product_data(stock=50)
# Returns: {id, name, description, price, stock, category, ...}
```

#### `mock_order_data(order_id=None, user_id=None, status="pending")`
Generate mock order data.

```python
order = mock_order_data(status="shipped")
# Returns: {id, user_id, status, total_amount, items, ...}
```

#### `mock_cart_data(cart_id=None, user_id=None, items_count=3)`
Generate mock shopping cart data.

```python
cart = mock_cart_data(items_count=5)
# Returns: {id, user_id, items, total, item_count, ...}
```

#### `mock_payment_data(payment_id=None, order_id=None, status="completed")`
Generate mock payment data.

```python
payment = mock_payment_data(status="completed")
# Returns: {id, order_id, amount, commission, status, ...}
```

#### `mock_review_data(review_id=None, product_id=None, user_id=None, rating=5)`
Generate mock review data.

```python
review = mock_review_data(rating=4)
# Returns: {id, product_id, user_id, rating, title, comment, ...}
```

#### `mock_notification_data(notification_id=None, user_id=None, notification_type="order_update")`
Generate mock notification data.

```python
notification = mock_notification_data(notification_type="payment_received")
# Returns: {id, user_id, type, title, message, read, ...}
```

### Mock API Responses

#### `mock_api_success_response(data)`
Generate a successful API response.

```python
response = mock_api_success_response({"message": "Success"})
# Returns: MockAPIResponse(status=200, body={success: True, data: ...})
```

#### `mock_api_error_response(message, status=400)`
Generate an error API response.

```python
response = mock_api_error_response("Invalid input", status=400)
# Returns: MockAPIResponse(status=400, body={success: False, error: ...})
```

#### `mock_authentication_success()`
Generate successful authentication response.

```python
auth = mock_authentication_success()
# Returns: {success, token, refresh_token, expires_in, user}
```

#### `mock_authentication_failure()`
Generate failed authentication response.

```python
auth = mock_authentication_failure()
# Returns: {success: False, error, message}
```

### Mock Route Handlers

#### `mock_api_route_handler(route, response_data, status=200)`
Route handler for API responses.

```python
async def handler(route):
    await mock_api_route_handler(route, {"data": "test"}, status=200)

await page.route("**/api/**", handler)
```

### Mock Services

#### `mock_database_connection()`
Create a mock database connection.

```python
db = mock_database_connection()
result = db.execute("SELECT * FROM users")
```

#### `mock_email_service()`
Create a mock email service.

```python
email = mock_email_service()
result = email.send("test@example.com", "Subject", "Body")
```

#### `mock_payment_gateway()`
Create a mock payment gateway.

```python
gateway = mock_payment_gateway()
result = gateway.process_payment(100.00)
```

#### `mock_storage_service()`
Create a mock storage service.

```python
storage = mock_storage_service()
result = storage.upload("file.jpg", file_data)
```

### Mock Utilities

#### `mock_search_results(query, count=10)`
Generate mock search results.

```python
results = mock_search_results("laptop", count=20)
# Returns: {query, total_results, results, facets}
```

#### `mock_performance_metrics()`
Generate mock performance metrics.

```python
metrics = mock_performance_metrics()
# Returns: {response_time, throughput, error_rate, ...}
```

#### `mock_network_delay(min_ms=100, max_ms=500)`
Simulate network delay.

```python
await mock_network_delay(200, 1000)
```

---

## Fixtures

### Browser Fixtures

#### `playwright_instance` (session scope)
Provides a Playwright instance for the entire test session.

```python
async def test_example(playwright_instance):
    # Use playwright_instance
```

#### `browser` (session scope)
Provides a browser instance for the entire test session.

```python
async def test_example(browser):
    # Use browser
```

#### `context` (function scope)
Provides a new browser context for each test.

```python
async def test_example(context):
    # Use context
```

#### `page` (function scope)
Provides a new page for each test.

```python
async def test_example(page):
    await page.goto("http://localhost:3000")
```

### Authentication Fixtures

#### `authenticated_page`
Provides a page with authentication cookies already set.

```python
async def test_dashboard(authenticated_page):
    await authenticated_page.goto("http://localhost:3000/dashboard")
```

### Mock Data Fixtures

#### `mock_user`, `mock_customer`, `mock_vendor`, `mock_admin`
Provides mock user data with different roles.

```python
def test_user_creation(mock_customer):
    assert mock_customer["role"] == "customer"
```

#### `mock_product`, `mock_products`
Provides mock product data (single or multiple).

```python
def test_product_display(mock_product):
    assert mock_product["price"] > 0
```

#### `mock_order`
Provides mock order data.

```python
def test_order_processing(mock_order):
    assert mock_order["status"] in ["pending", "processing"]
```

#### `mock_cart`
Provides mock shopping cart data.

```python
def test_cart_total(mock_cart):
    assert mock_cart["total"] > 0
```

### Utility Fixtures

#### `base_url`
Provides the base URL for tests.

```python
async def test_homepage(page, base_url):
    await page.goto(base_url)
```

#### `test_credentials`
Provides test user credentials.

```python
async def test_login(page, test_credentials):
    email = test_credentials["customer"]["email"]
    password = test_credentials["customer"]["password"]
```

#### `performance_tracker`
Track performance metrics during tests.

```python
def test_performance(performance_tracker):
    performance_tracker["start"]()
    # ... test code
    performance_tracker["stop"]()
    assert performance_tracker["duration"] < 5.0
```

#### `console_logger`
Capture console messages during tests.

```python
async def test_with_console(page, console_logger):
    await page.goto("http://localhost:3000")
    # console_logger contains all console messages
```

#### `network_logger`
Capture network requests during tests.

```python
async def test_api_calls(page, network_logger):
    await page.goto("http://localhost:3000")
    # network_logger contains all network requests
```

---

## Usage Examples

### Example 1: Basic Test with Stubs

```python
import asyncio
from test_stubs import stub_full_page_setup, stub_cleanup, stub_fill_input

async def test_login():
    pw, browser, context, page = await stub_full_page_setup()

    try:
        await stub_fill_input(page, "#email", "test@example.com")
        await stub_fill_input(page, "#password", "password123")
        # ... rest of test
    finally:
        await stub_cleanup(context, browser, pw)

asyncio.run(test_login())
```

### Example 2: Test with Mock Data

```python
from test_mocks import mock_user_data, mock_api_route_handler

async def test_user_registration():
    user = mock_user_data(email="newuser@test.com")

    async def api_handler(route):
        await mock_api_route_handler(route, {"success": True, "user": user})

    # Use in your test
```

### Example 3: Pytest Test with Fixtures

```python
import pytest
from playwright.async_api import expect

@pytest.mark.asyncio
async def test_product_page(page, mock_product, base_url):
    await page.goto(f"{base_url}/products/{mock_product['id']}")
    await expect(page.locator(f"text={mock_product['name']}")).to_be_visible()
```

### Example 4: Mocking API Responses

```python
from test_mocks import mock_product_data, mock_api_route_handler

async def test_with_mocked_api(page):
    products = [mock_product_data() for _ in range(5)]

    async def handle_products(route):
        if "/api/products" in route.request.url:
            await mock_api_route_handler(route, products)
        else:
            await route.continue_()

    await page.route("**/api/**", handle_products)
    await page.goto("http://localhost:3000/products")
```

---

## Best Practices

### 1. Use Stubs for Common Operations
Instead of repeating setup code, use stubs:

```python
# Good
pw, browser, context, page = await stub_full_page_setup()

# Avoid
pw = await async_playwright().start()
browser = await pw.chromium.launch(...)
# ... lots of repetitive code
```

### 2. Use Mocks for External Dependencies
Mock external services to make tests reliable and fast:

```python
# Good - uses mocks
async def handle_api(route):
    await mock_api_route_handler(route, mock_user_data())

# Avoid - depends on real API
# Real API calls make tests slow and flaky
```

### 3. Use Fixtures for Common Setup
Let pytest fixtures handle setup and teardown:

```python
# Good
async def test_example(page, mock_user):
    # page and mock_user are automatically provided

# Avoid manually creating everything in each test
```

### 4. Combine Stubs and Mocks
Use both together for comprehensive testing:

```python
async def test_checkout():
    # Use stub for setup
    pw, browser, context, page = await stub_full_page_setup()

    # Use mock for data
    cart = mock_cart_data(items_count=3)

    # Use stub for interaction
    await stub_click_element(page, "#checkout")
```

### 5. Clean Up Resources
Always clean up in the finally block:

```python
try:
    # Test code
    pass
finally:
    await stub_cleanup(context, browser, pw)
```

### 6. Use Appropriate Timeouts
Different operations need different timeouts:

```python
await stub_wait_for_selector(page, "text=Loading", timeout=3000)  # Short
await stub_wait_for_selector(page, "text=Success", timeout=30000)  # Long
```

---

## Running Tests

### Run all tests
```bash
pytest testsprite_tests/
```

### Run specific test file
```bash
pytest testsprite_tests/TC001_User_Registration_with_Valid_Data.py
```

### Run with markers
```bash
pytest -m smoke  # Run only smoke tests
pytest -m "not slow"  # Skip slow tests
```

### Run example usage
```bash
python testsprite_tests/example_usage.py
```

---

## File Structure

```
testsprite_tests/
├── test_stubs.py           # Stub functions
├── test_mocks.py           # Mock functions
├── test_fixtures.py        # Pytest fixtures
├── conftest.py             # Pytest configuration
├── example_usage.py        # Usage examples
├── STUBS_MOCKS_README.md   # This documentation
└── TC0XX_*.py              # Your test files
```

---

## Additional Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Async/Await](https://docs.python.org/3/library/asyncio.html)

---

## Support

For issues or questions:
1. Check this documentation
2. Review example_usage.py for working examples
3. Consult the inline code documentation in each module
