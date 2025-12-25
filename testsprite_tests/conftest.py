"""
Pytest Configuration File
Makes fixtures automatically available to all test files
"""
import sys
import os

# Add the test directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all fixtures to make them available
from test_fixtures import *

# Configure pytest
def pytest_configure(config):
    """Configure pytest with custom markers and settings"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", "smoke: marks tests as smoke tests"
    )
