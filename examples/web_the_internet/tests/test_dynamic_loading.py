import pytest
from automation_framework.src.core.base.web_test_base import WebTestBase
from examples.web_the_internet.pages.dynamic_loading_page import DynamicLoadingPage

class TestDynamicLoading(WebTestBase):
    
    @pytest.fixture
    def dynamic_loading_page(self, browser):
        return DynamicLoadingPage(browser)
    
    def test_example_1_hidden_element(self, dynamic_loading_page):
        """Test dynamic loading example 1 - element hidden on page."""
        # Navigate to example 1
        dynamic_loading_page.navigate_to_example(1)
        
        # Verify finish element is not visible initially
        assert dynamic_loading_page.is_finish_element_displayed() == False, "Finish element should not be visible initially"
        
        # Click start button
        dynamic_loading_page.click_start()
        
        # Wait for loading to complete
        dynamic_loading_page.wait_for_loading_to_complete()
        
        # Verify the finish element is now displayed with correct text
        assert dynamic_loading_page.is_finish_element_displayed() == True, "Finish element should be visible after loading"
        assert dynamic_loading_page.get_finish_text() == "Hello World!", "Finish element text should be 'Hello World!'"
    
    def test_example_2_rendered_element(self, dynamic_loading_page):
        """Test dynamic loading example 2 - element rendered after loading."""
        # Navigate to example 2
        dynamic_loading_page.navigate_to_example(2)
        
        # Click start button
        dynamic_loading_page.click_start()
        
        # Wait for loading to complete
        dynamic_loading_page.wait_for_loading_to_complete()
        
        # Verify the finish element is displayed with correct text
        assert dynamic_loading_page.is_finish_element_displayed() == True, "Finish element should be visible after loading"
        assert dynamic_loading_page.get_finish_text() == "Hello World!", "Finish element text should be 'Hello World!'"