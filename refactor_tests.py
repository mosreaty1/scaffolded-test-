#!/usr/bin/env python3
"""
Script to refactor all remaining test files to use stubs and mocks
"""
import os
import re

# Template for refactored test file header
TEMPLATE_HEADER = '''import asyncio
from playwright.async_api import expect

# Import stub functions for common operations
from test_stubs import (
    stub_full_page_setup,
    stub_cleanup,
    stub_async_sleep
)

# Import mock functions for test data
from test_mocks import (
    mock_user_data,
    mock_product_data,
    mock_order_data,
    mock_cart_data,
    mock_payment_data,
    mock_review_data,
    mock_notification_data
)
'''

# Test file descriptions
TEST_DESCRIPTIONS = {
    'TC011': 'Checkout Flow with Order Splitting and Stock Verification',
    'TC012': 'Order History and Sub-Order Status Display',
    'TC013': 'Payment Processing with Commission Deduction and Payout Tracking',
    'TC014': 'Review Submission and Display',
    'TC015': 'Notification Delivery and Preference Management',
    'TC016': 'Admin Dashboard User and Vendor Management',
    'TC017': 'Performance Testing for Marketplace Search Response',
    'TC018': 'Security Test - Access Unauthorized Pages',
    'TC019': 'Shopping Cart Persistence Across Sessions',
    'TC020': 'Order Checkout with Insufficient Stock'
}

def refactor_test_file(filepath):
    """Refactor a single test file"""
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract test case number
    filename = os.path.basename(filepath)
    tc_match = re.search(r'TC(\d+)', filename)
    if not tc_match:
        return False

    tc_num = f'TC{tc_match.group(1)}'
    description = TEST_DESCRIPTIONS.get(tc_num, 'Test case')

    # Find the async def run_test(): line and everything after it
    run_test_match = re.search(r'(async def run_test\(\):.*)', content, re.DOTALL)
    if not run_test_match:
        return False

    run_test_content = run_test_match.group(1)

    # Replace the old setup code
    new_run_test = re.sub(
        r'pw = None\s+browser = None\s+context = None\s+try:\s+# Start a Playwright.*?pass\s+# Iterate.*?pass',
        f'''pw = None
    browser = None
    context = None

    try:
        # Use stub for complete page setup
        pw, browser, context, page = await stub_full_page_setup(
            url="http://localhost:3000",
            headless=True,
            default_timeout=5000
        )

        # Mock data for {description}
        # TODO: Customize mock data as needed for this test''',
        run_test_content,
        flags=re.DOTALL
    )

    # Replace asyncio.sleep with stub_async_sleep
    new_run_test = re.sub(
        r'await asyncio\.sleep\((\d+)\)',
        r'await stub_async_sleep(\1)',
        new_run_test
    )

    # Replace cleanup code
    new_run_test = re.sub(
        r'finally:\s+if context:.*?await pw\.stop\(\)',
        '''finally:
        # Use stub for cleanup
        await stub_cleanup(context, browser, pw)''',
        new_run_test,
        flags=re.DOTALL
    )

    # Add docstring
    new_run_test = re.sub(
        r'async def run_test\(\):',
        f'''async def run_test():
    """
    {tc_num}: {description}
    """''',
        new_run_test
    )

    # Combine header and function
    new_content = TEMPLATE_HEADER + '\n' + new_run_test

    # Write back
    with open(filepath, 'w') as f:
        f.write(new_content)

    print(f"Refactored: {filename}")
    return True

def main():
    """Main function"""
    test_dir = 'testsprite_tests'
    test_files = [
        'TC011_Checkout_Flow_with_Order_Splitting_and_Stock_Verification.py',
        'TC012_Order_History_and_Sub_Order_Status_Display.py',
        'TC013_Payment_Processing_with_Commission_Deduction_and_Payout_Tracking.py',
        'TC014_Review_Submission_and_Display.py',
        'TC015_Notification_Delivery_and_Preference_Management.py',
        'TC016_Admin_Dashboard_User_and_Vendor_Management.py',
        'TC017_Performance_Testing_for_Marketplace_Search_Response.py',
        'TC018_Security_Test___Access_Unauthorized_Pages.py',
        'TC019_Shopping_Cart_Persistence_Across_Sessions.py',
        'TC020_Order_Checkout_with_Insufficient_Stock.py'
    ]

    for test_file in test_files:
        filepath = os.path.join(test_dir, test_file)
        if os.path.exists(filepath):
            refactor_test_file(filepath)

    print("\nAll test files refactored successfully!")

if __name__ == '__main__':
    main()
