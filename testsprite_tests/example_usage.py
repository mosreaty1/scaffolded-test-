"""
Example Usage of Stubs and Mocks
Demonstrates how to use the test_stubs and test_mocks modules
"""
import asyncio
from playwright.async_api import expect

# Import stub functions
from test_stubs import (
    stub_full_page_setup,
    stub_cleanup,
    stub_click_element,
    stub_fill_input,
    stub_wait_for_selector,
    stub_async_sleep
)

# Import mock functions
from test_mocks import (
    mock_user_data,
    mock_product_data,
    mock_authentication_success,
    mock_api_route_handler,
    mock_cart_data
)


async def example_test_with_stubs():
    """
    Example: Using stub functions for test setup
    """
    pw = None
    browser = None
    context = None
    page = None

    try:
        # Use stub for complete page setup
        pw, browser, context, page = await stub_full_page_setup(
            url="http://localhost:3000",
            headless=True
        )

        # Use stub functions for interactions
        await stub_wait_for_selector(page, "text=Welcome")
        await stub_fill_input(page, "#email", "test@example.com")
        await stub_fill_input(page, "#password", "Test123456!")
        await stub_click_element(page, "button[type='submit']")

        # Use stub for async sleep
        await stub_async_sleep(2)

        # Assertions
        await expect(page.locator("text=Dashboard")).to_be_visible(timeout=10000)

        print("Test passed: User login successful")

    finally:
        # Use stub for cleanup
        await stub_cleanup(context, browser, pw)


async def example_test_with_mocks():
    """
    Example: Using mock functions for API responses
    """
    pw = None
    browser = None
    context = None
    page = None

    try:
        pw, browser, context, page = await stub_full_page_setup()

        # Mock user data
        user = mock_user_data(email="mockuser@test.com", role="customer")
        print(f"Mock user created: {user['email']}")

        # Mock authentication response
        auth_response = mock_authentication_success()
        print(f"Mock auth token: {auth_response['token'][:20]}...")

        # Mock product data
        product = mock_product_data(stock=50)
        print(f"Mock product: {product['name']} - ${product['price']}")

        # Mock cart data
        cart = mock_cart_data(items_count=3)
        print(f"Mock cart total: ${cart['total']}")

        # Intercept API calls and return mock data
        async def handle_api_route(route):
            if "/api/auth/login" in route.request.url:
                await mock_api_route_handler(route, auth_response)
            elif "/api/products" in route.request.url:
                await mock_api_route_handler(route, [product])
            elif "/api/cart" in route.request.url:
                await mock_api_route_handler(route, cart)
            else:
                await route.continue_()

        await page.route("**/api/**", handle_api_route)

        # Navigate and interact with mocked APIs
        await page.goto("http://localhost:3000")

        print("Test completed with mock data")

    finally:
        await stub_cleanup(context, browser, pw)


async def example_combined_test():
    """
    Example: Combining stubs and mocks in a single test
    """
    pw = None
    browser = None
    context = None
    page = None

    try:
        # Setup using stubs
        pw, browser, context, page = await stub_full_page_setup()

        # Create mock data
        vendor = mock_user_data(role="vendor")
        product = mock_product_data(vendor_id=vendor["id"])

        # Mock API responses
        async def api_handler(route):
            url = route.request.url
            if "/api/products/create" in url:
                await mock_api_route_handler(
                    route,
                    {"success": True, "product": product}
                )
            else:
                await route.continue_()

        await page.route("**/api/**", api_handler)

        # Perform actions using stubs
        await stub_wait_for_selector(page, "#product-name")
        await stub_fill_input(page, "#product-name", product["name"])
        await stub_fill_input(page, "#product-price", str(product["price"]))
        await stub_click_element(page, "button#create-product")

        # Wait and verify
        await stub_async_sleep(2)
        await expect(page.locator("text=Product created successfully")).to_be_visible()

        print("Combined test passed successfully")

    finally:
        await stub_cleanup(context, browser, pw)


# Example pytest test using fixtures
async def test_example_with_fixtures(page, mock_user, mock_product):
    """
    Example: Using pytest fixtures (requires pytest to run)
    This shows how fixtures automatically provide page and mock data
    """
    print(f"Testing with user: {mock_user['email']}")
    print(f"Testing with product: {mock_product['name']}")

    # Your test code here using the fixtures
    await page.goto("http://localhost:3000")
    # ... rest of test


if __name__ == "__main__":
    print("Running example tests...\n")

    print("=" * 50)
    print("Example 1: Test with Stubs")
    print("=" * 50)
    asyncio.run(example_test_with_stubs())

    print("\n" + "=" * 50)
    print("Example 2: Test with Mocks")
    print("=" * 50)
    asyncio.run(example_test_with_mocks())

    print("\n" + "=" * 50)
    print("Example 3: Combined Test")
    print("=" * 50)
    asyncio.run(example_combined_test())

    print("\n" + "=" * 50)
    print("All examples completed!")
    print("=" * 50)
