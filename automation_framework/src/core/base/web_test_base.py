import pytest
from ...web.drivers.browser_factory import BrowserFactory

class WebTestBase:
    @pytest.fixture(scope="function")
    def browser(self, request):
        # Get browser type with a fallback
        try:
            browser_type = request.config.getoption("--browser")
        except (ValueError, AttributeError):
            browser_type = "chrome"
            
        # Get headless mode with a fallback
        try:
            headless = request.config.getoption("--headless")
        except (ValueError, AttributeError):
            headless = False
            
        # Initialize browser
        driver = BrowserFactory.get_browser(browser_type, headless)
        
        # Set implicit wait
        driver.implicitly_wait(10)
        
        # Return browser to test
        yield driver
        
        # Teardown
        driver.quit()