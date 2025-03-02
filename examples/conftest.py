import pytest

def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="Browser to run tests on")
    parser.addoption("--headless", action="store_true", help="Run browser in headless mode")