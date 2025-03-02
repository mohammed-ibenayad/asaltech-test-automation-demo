import pytest
from ...web.drivers.browser_factory import BrowserFactory

class WebTestBase:
    @pytest.fixture(scope="function")
    def browser(self, request):
        # Get browser type from pytest config or use default
        browser_type = getattr(request.config, "browser", "chrome")
        headless = getattr(request.config, "headless", False)
        
        # Initialize browser
        driver = BrowserFactory.get_browser(browser_type, headless)
        
        # Set implicit wait
        driver.implicitly_wait(10)
        
        # Return browser to test
        yield driver
        
        # Teardown
        driver.quit()