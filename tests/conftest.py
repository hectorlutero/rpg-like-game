import pytest

def pytest_addoption(parser):
    parser.addoption("--watch", action="store_true", default=False, help="Run E2E tests visually with delays")
