import pytest
from selenium.webdriver.common.by import By
from automation_framework.src.core.base.web_test_base import WebTestBase
from examples.web_example.pages.login_page import LoginPage

class TestLogin(WebTestBase):
    
    @pytest.fixture
    def login_page(self, browser):
        return LoginPage(browser)
    
    def test_valid_login(self, login_page):
        """Test successful login with valid credentials."""
        login_page.navigate()
        login_page.login("tomsmith", "SuperSecretPassword!")
        assert login_page.is_login_successful() == True
    
    def test_invalid_login(self, login_page):
        """Test failed login with invalid credentials."""
        login_page.navigate()
        login_page.login("invalid", "invalid")
        assert login_page.is_login_successful() == False
        assert "invalid" in login_page.get_error_message().lower()