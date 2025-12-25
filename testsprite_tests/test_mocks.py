"""
Test Mocks Module
Contains mock functions for external dependencies and API responses
"""
from typing import Any, Dict, List, Optional, Callable
from unittest.mock import Mock, AsyncMock, MagicMock
from playwright.async_api import Page, Route, Request
import json
import random
import string
from datetime import datetime, timedelta


class MockAPIResponse:
    """Mock API response object"""

    def __init__(
        self,
        status: int = 200,
        body: Any = None,
        headers: Optional[Dict[str, str]] = None
    ):
        self.status = status
        self.body = body or {}
        self.headers = headers or {"Content-Type": "application/json"}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "body": json.dumps(self.body) if isinstance(self.body, (dict, list)) else self.body,
            "headers": self.headers
        }


def mock_user_data(
    user_id: Optional[str] = None,
    email: Optional[str] = None,
    role: str = "customer"
) -> Dict[str, Any]:
    """
    Mock: Generate mock user data

    Args:
        user_id: User ID (auto-generated if None)
        email: User email (auto-generated if None)
        role: User role (customer, vendor, admin)

    Returns: Mock user data dictionary
    """
    uid = user_id or f"user_{random.randint(1000, 9999)}"
    return {
        "id": uid,
        "email": email or f"test_{uid}@example.com",
        "username": f"user_{uid}",
        "role": role,
        "first_name": "Test",
        "last_name": "User",
        "created_at": datetime.now().isoformat(),
        "is_active": True,
        "profile": {
            "phone": "+1234567890",
            "address": "123 Test Street",
            "city": "Test City",
            "country": "Test Country"
        }
    }


def mock_product_data(
    product_id: Optional[str] = None,
    vendor_id: Optional[str] = None,
    stock: int = 100
) -> Dict[str, Any]:
    """
    Mock: Generate mock product data

    Args:
        product_id: Product ID (auto-generated if None)
        vendor_id: Vendor ID (auto-generated if None)
        stock: Available stock quantity

    Returns: Mock product data dictionary
    """
    pid = product_id or f"prod_{random.randint(1000, 9999)}"
    vid = vendor_id or f"vendor_{random.randint(100, 999)}"
    return {
        "id": pid,
        "name": f"Test Product {pid}",
        "description": "This is a test product description",
        "price": round(random.uniform(10.0, 500.0), 2),
        "stock": stock,
        "category": random.choice(["Electronics", "Clothing", "Home", "Books"]),
        "vendor_id": vid,
        "images": [
            f"https://example.com/images/{pid}_1.jpg",
            f"https://example.com/images/{pid}_2.jpg"
        ],
        "rating": round(random.uniform(3.0, 5.0), 1),
        "reviews_count": random.randint(0, 500),
        "created_at": datetime.now().isoformat(),
        "is_active": True
    }


def mock_order_data(
    order_id: Optional[str] = None,
    user_id: Optional[str] = None,
    status: str = "pending"
) -> Dict[str, Any]:
    """
    Mock: Generate mock order data

    Args:
        order_id: Order ID (auto-generated if None)
        user_id: User ID (auto-generated if None)
        status: Order status (pending, processing, shipped, delivered, cancelled)

    Returns: Mock order data dictionary
    """
    oid = order_id or f"order_{random.randint(10000, 99999)}"
    uid = user_id or f"user_{random.randint(1000, 9999)}"
    return {
        "id": oid,
        "user_id": uid,
        "status": status,
        "total_amount": round(random.uniform(50.0, 1000.0), 2),
        "subtotal": round(random.uniform(40.0, 900.0), 2),
        "tax": round(random.uniform(5.0, 100.0), 2),
        "shipping": round(random.uniform(5.0, 20.0), 2),
        "items": [
            {
                "product_id": f"prod_{random.randint(1000, 9999)}",
                "quantity": random.randint(1, 5),
                "price": round(random.uniform(10.0, 200.0), 2)
            }
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }


def mock_payment_data(
    payment_id: Optional[str] = None,
    order_id: Optional[str] = None,
    status: str = "completed"
) -> Dict[str, Any]:
    """
    Mock: Generate mock payment data

    Args:
        payment_id: Payment ID (auto-generated if None)
        order_id: Order ID (auto-generated if None)
        status: Payment status (pending, completed, failed, refunded)

    Returns: Mock payment data dictionary
    """
    pid = payment_id or f"pay_{random.randint(10000, 99999)}"
    oid = order_id or f"order_{random.randint(10000, 99999)}"
    return {
        "id": pid,
        "order_id": oid,
        "amount": round(random.uniform(50.0, 1000.0), 2),
        "commission": round(random.uniform(5.0, 100.0), 2),
        "status": status,
        "payment_method": random.choice(["credit_card", "paypal", "stripe"]),
        "transaction_id": f"txn_{''.join(random.choices(string.ascii_uppercase + string.digits, k=16))}",
        "processed_at": datetime.now().isoformat()
    }


def mock_review_data(
    review_id: Optional[str] = None,
    product_id: Optional[str] = None,
    user_id: Optional[str] = None,
    rating: int = 5
) -> Dict[str, Any]:
    """
    Mock: Generate mock review data

    Args:
        review_id: Review ID (auto-generated if None)
        product_id: Product ID (auto-generated if None)
        user_id: User ID (auto-generated if None)
        rating: Review rating (1-5)

    Returns: Mock review data dictionary
    """
    rid = review_id or f"review_{random.randint(1000, 9999)}"
    pid = product_id or f"prod_{random.randint(1000, 9999)}"
    uid = user_id or f"user_{random.randint(1000, 9999)}"
    return {
        "id": rid,
        "product_id": pid,
        "user_id": uid,
        "rating": rating,
        "title": "Great product!",
        "comment": "This is a test review comment.",
        "created_at": datetime.now().isoformat(),
        "helpful_count": random.randint(0, 50)
    }


def mock_notification_data(
    notification_id: Optional[str] = None,
    user_id: Optional[str] = None,
    notification_type: str = "order_update"
) -> Dict[str, Any]:
    """
    Mock: Generate mock notification data

    Args:
        notification_id: Notification ID (auto-generated if None)
        user_id: User ID (auto-generated if None)
        notification_type: Type of notification

    Returns: Mock notification data dictionary
    """
    nid = notification_id or f"notif_{random.randint(1000, 9999)}"
    uid = user_id or f"user_{random.randint(1000, 9999)}"
    return {
        "id": nid,
        "user_id": uid,
        "type": notification_type,
        "title": "Test Notification",
        "message": "This is a test notification message.",
        "read": False,
        "created_at": datetime.now().isoformat()
    }


async def mock_api_route_handler(
    route: Route,
    response_data: Any,
    status: int = 200
) -> None:
    """
    Mock: Route handler for API responses

    Args:
        route: Playwright route object
        response_data: Response data to return
        status: HTTP status code
    """
    await route.fulfill(
        status=status,
        body=json.dumps(response_data),
        headers={"Content-Type": "application/json"}
    )


def mock_api_success_response(data: Any) -> MockAPIResponse:
    """
    Mock: Generate a successful API response

    Args:
        data: Response data

    Returns: MockAPIResponse object
    """
    return MockAPIResponse(status=200, body={"success": True, "data": data})


def mock_api_error_response(
    message: str,
    status: int = 400
) -> MockAPIResponse:
    """
    Mock: Generate an error API response

    Args:
        message: Error message
        status: HTTP status code

    Returns: MockAPIResponse object
    """
    return MockAPIResponse(
        status=status,
        body={"success": False, "error": message}
    )


def mock_authentication_success() -> Dict[str, Any]:
    """
    Mock: Generate successful authentication response

    Returns: Authentication response dictionary
    """
    return {
        "success": True,
        "token": f"mock_token_{''.join(random.choices(string.ascii_letters + string.digits, k=32))}",
        "refresh_token": f"mock_refresh_{''.join(random.choices(string.ascii_letters + string.digits, k=32))}",
        "expires_in": 3600,
        "user": mock_user_data()
    }


def mock_authentication_failure() -> Dict[str, Any]:
    """
    Mock: Generate failed authentication response

    Returns: Authentication error dictionary
    """
    return {
        "success": False,
        "error": "Invalid credentials",
        "message": "The email or password you entered is incorrect"
    }


def mock_cart_data(
    cart_id: Optional[str] = None,
    user_id: Optional[str] = None,
    items_count: int = 3
) -> Dict[str, Any]:
    """
    Mock: Generate mock shopping cart data

    Args:
        cart_id: Cart ID (auto-generated if None)
        user_id: User ID (auto-generated if None)
        items_count: Number of items in cart

    Returns: Mock cart data dictionary
    """
    cid = cart_id or f"cart_{random.randint(1000, 9999)}"
    uid = user_id or f"user_{random.randint(1000, 9999)}"
    items = []
    total = 0.0

    for _ in range(items_count):
        price = round(random.uniform(10.0, 200.0), 2)
        quantity = random.randint(1, 5)
        items.append({
            "product_id": f"prod_{random.randint(1000, 9999)}",
            "product_name": f"Test Product {random.randint(1, 100)}",
            "price": price,
            "quantity": quantity,
            "subtotal": round(price * quantity, 2),
            "vendor_id": f"vendor_{random.randint(100, 999)}"
        })
        total += price * quantity

    return {
        "id": cid,
        "user_id": uid,
        "items": items,
        "total": round(total, 2),
        "item_count": items_count,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }


def mock_database_connection() -> Mock:
    """
    Mock: Create a mock database connection

    Returns: Mock database connection object
    """
    mock_db = Mock()
    mock_db.connect = Mock(return_value=True)
    mock_db.disconnect = Mock(return_value=True)
    mock_db.execute = Mock(return_value={"success": True})
    mock_db.fetch_one = Mock(return_value=mock_user_data())
    mock_db.fetch_all = Mock(return_value=[mock_user_data() for _ in range(5)])
    return mock_db


async def mock_async_database_connection() -> AsyncMock:
    """
    Mock: Create a mock async database connection

    Returns: AsyncMock database connection object
    """
    mock_db = AsyncMock()
    mock_db.connect = AsyncMock(return_value=True)
    mock_db.disconnect = AsyncMock(return_value=True)
    mock_db.execute = AsyncMock(return_value={"success": True})
    mock_db.fetch_one = AsyncMock(return_value=mock_user_data())
    mock_db.fetch_all = AsyncMock(return_value=[mock_user_data() for _ in range(5)])
    return mock_db


def mock_email_service() -> Mock:
    """
    Mock: Create a mock email service

    Returns: Mock email service object
    """
    mock_email = Mock()
    mock_email.send = Mock(return_value={"success": True, "message_id": f"msg_{random.randint(1000, 9999)}"})
    mock_email.send_bulk = Mock(return_value={"success": True, "sent_count": 10})
    return mock_email


def mock_payment_gateway() -> Mock:
    """
    Mock: Create a mock payment gateway

    Returns: Mock payment gateway object
    """
    mock_gateway = Mock()
    mock_gateway.process_payment = Mock(return_value=mock_payment_data(status="completed"))
    mock_gateway.refund_payment = Mock(return_value={"success": True, "refund_id": f"ref_{random.randint(1000, 9999)}"})
    mock_gateway.verify_payment = Mock(return_value={"verified": True})
    return mock_gateway


def mock_storage_service() -> Mock:
    """
    Mock: Create a mock storage service (e.g., S3, Azure Blob)

    Returns: Mock storage service object
    """
    mock_storage = Mock()
    mock_storage.upload = Mock(return_value={"success": True, "url": "https://example.com/uploads/test.jpg"})
    mock_storage.download = Mock(return_value=b"mock file content")
    mock_storage.delete = Mock(return_value={"success": True})
    return mock_storage


def mock_search_results(query: str, count: int = 10) -> Dict[str, Any]:
    """
    Mock: Generate mock search results

    Args:
        query: Search query
        count: Number of results to generate

    Returns: Mock search results dictionary
    """
    return {
        "query": query,
        "total_results": count,
        "results": [mock_product_data() for _ in range(count)],
        "facets": {
            "categories": ["Electronics", "Clothing", "Home", "Books"],
            "price_ranges": ["0-50", "50-100", "100-500", "500+"]
        }
    }


def mock_performance_metrics() -> Dict[str, Any]:
    """
    Mock: Generate mock performance metrics

    Returns: Mock performance metrics dictionary
    """
    return {
        "response_time": round(random.uniform(50, 500), 2),
        "throughput": random.randint(100, 1000),
        "error_rate": round(random.uniform(0, 5), 2),
        "cpu_usage": round(random.uniform(10, 80), 2),
        "memory_usage": round(random.uniform(20, 90), 2),
        "timestamp": datetime.now().isoformat()
    }


async def mock_network_delay(min_ms: int = 100, max_ms: int = 500) -> None:
    """
    Mock: Simulate network delay

    Args:
        min_ms: Minimum delay in milliseconds
        max_ms: Maximum delay in milliseconds
    """
    import asyncio
    delay = random.uniform(min_ms, max_ms) / 1000
    await asyncio.sleep(delay)


def mock_page_element(
    tag: str = "div",
    text: Optional[str] = None,
    attributes: Optional[Dict[str, str]] = None
) -> Mock:
    """
    Mock: Create a mock page element

    Args:
        tag: HTML tag name
        text: Element text content
        attributes: Element attributes

    Returns: Mock element object
    """
    mock_element = Mock()
    mock_element.tag_name = tag
    mock_element.text_content = Mock(return_value=text or "Mock element text")
    mock_element.get_attribute = Mock(side_effect=lambda attr: (attributes or {}).get(attr))
    mock_element.click = AsyncMock()
    mock_element.fill = AsyncMock()
    mock_element.is_visible = Mock(return_value=True)
    return mock_element


def create_mock_locator(text: str = "Mock Text") -> Mock:
    """
    Mock: Create a mock Playwright locator

    Args:
        text: Text content of the locator

    Returns: Mock locator object
    """
    mock_locator = Mock()
    mock_locator.first = mock_locator
    mock_locator.text_content = AsyncMock(return_value=text)
    mock_locator.is_visible = AsyncMock(return_value=True)
    mock_locator.click = AsyncMock()
    mock_locator.fill = AsyncMock()
    mock_locator.count = AsyncMock(return_value=1)
    return mock_locator
