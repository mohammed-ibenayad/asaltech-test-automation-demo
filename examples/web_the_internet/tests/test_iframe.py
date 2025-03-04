import pytest
from automation_framework.src.core.base.web_test_base import WebTestBase
from examples.web_the_internet.pages.iframe_page import IFramePage

class TestIFrame(WebTestBase):
    
    @pytest.fixture
    def iframe_page(self, browser):
        """Fixture to create an instance of the IFramePage"""
        return IFramePage(browser)
    
    def test_iframe_editor_basic_interaction(self, iframe_page):
        """Test basic interaction with the TinyMCE editor inside an iframe"""
        # Navigate to the iframe page
        iframe_page.navigate()
        
        # Get the default text
        default_text = iframe_page.get_editor_text()
        assert "Your content goes here." in default_text, "Default text not found in editor"
        
        # Clear the editor
        iframe_page.clear_editor()
        
        # Type new text
        test_text = "This is a test of the iframe editor."
        iframe_page.type_text(test_text)
        
        # Verify the text was entered correctly
        current_text = iframe_page.get_editor_text()
        assert test_text in current_text, f"Expected '{test_text}' but got '{current_text}'"
    
    def test_iframe_editor_text_formatting(self, iframe_page):
        """Test formatting text in the TinyMCE editor"""
        # Navigate to the iframe page
        iframe_page.navigate()
        
        # Clear the editor
        iframe_page.clear_editor()
        
        # Type new text
        test_text = "This text will be bold."
        iframe_page.type_text(test_text)
        
        # Select all text
        iframe_page.select_all_text()
        
        # Apply bold formatting
        iframe_page.format_bold()
        
        # Verify the text is still there after formatting
        current_text = iframe_page.get_editor_text()
        assert test_text in current_text, f"Text should remain after formatting. Expected '{test_text}' but got '{current_text}'"
        
        # Note: Verifying that text is actually bold would require checking HTML elements
        # This would be a more advanced test case