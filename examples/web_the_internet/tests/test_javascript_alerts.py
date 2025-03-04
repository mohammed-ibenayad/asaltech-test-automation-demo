import pytest
from automation_framework.src.core.base.web_test_base import WebTestBase
from examples.web_the_internet.pages.javascript_alerts_page import JavaScriptAlertsPage

class TestJavaScriptAlerts(WebTestBase):
    
    @pytest.fixture
    def js_alerts_page(self, browser):
        """Fixture to create an instance of the JavaScriptAlertsPage"""
        return JavaScriptAlertsPage(browser)
    
    def test_js_alert(self, js_alerts_page):
        """Test handling a basic JavaScript alert"""
        # Navigate to the JavaScript Alerts page
        js_alerts_page.navigate()
        
        # Click the button to trigger the alert
        js_alerts_page.click_js_alert_button()
        
        # Verify the alert text
        alert_text = js_alerts_page.get_alert_text()
        assert alert_text == "I am a JS Alert", f"Expected 'I am a JS Alert' but got '{alert_text}'"
        
        # Accept the alert
        js_alerts_page.accept_alert()
        
        # Verify the result text
        result_text = js_alerts_page.get_result_text()
        assert "You successfully clicked an alert" in result_text, \
            f"Expected success message but got '{result_text}'"
    
    def test_js_confirm_accept(self, js_alerts_page):
        """Test accepting a JavaScript confirm dialog"""
        # Navigate to the JavaScript Alerts page
        js_alerts_page.navigate()
        
        # Click the button to trigger the confirm dialog
        js_alerts_page.click_js_confirm_button()
        
        # Verify the confirm dialog text
        confirm_text = js_alerts_page.get_alert_text()
        assert confirm_text == "I am a JS Confirm", \
            f"Expected 'I am a JS Confirm' but got '{confirm_text}'"
        
        # Accept the confirm dialog
        js_alerts_page.accept_alert()
        
        # Verify the result text
        result_text = js_alerts_page.get_result_text()
        assert "You clicked: Ok" in result_text, \
            f"Expected 'You clicked: Ok' but got '{result_text}'"
    
    def test_js_confirm_dismiss(self, js_alerts_page):
        """Test dismissing a JavaScript confirm dialog"""
        # Navigate to the JavaScript Alerts page
        js_alerts_page.navigate()
        
        # Click the button to trigger the confirm dialog
        js_alerts_page.click_js_confirm_button()
        
        # Dismiss the confirm dialog
        js_alerts_page.dismiss_alert()
        
        # Verify the result text
        result_text = js_alerts_page.get_result_text()
        assert "You clicked: Cancel" in result_text, \
            f"Expected 'You clicked: Cancel' but got '{result_text}'"
    
    def test_js_prompt(self, js_alerts_page):
        """Test entering text in a JavaScript prompt dialog"""
        # Navigate to the JavaScript Alerts page
        js_alerts_page.navigate()
        
        # Click the button to trigger the prompt dialog
        js_alerts_page.click_js_prompt_button()
        
        # Verify the prompt dialog text
        prompt_text = js_alerts_page.get_alert_text()
        assert prompt_text == "I am a JS prompt", \
            f"Expected 'I am a JS prompt' but got '{prompt_text}'"
        
        # Enter text into the prompt
        test_input = "Test automation is fun!"
        js_alerts_page.enter_prompt_text(test_input)
        
        # Accept the prompt
        js_alerts_page.accept_alert()
        
        # Verify the result text
        result_text = js_alerts_page.get_result_text()
        assert f"You entered: {test_input}" in result_text, \
            f"Expected 'You entered: {test_input}' but got '{result_text}'"
    
    def test_js_prompt_dismiss(self, js_alerts_page):
        """Test dismissing a JavaScript prompt dialog"""
        # Navigate to the JavaScript Alerts page
        js_alerts_page.navigate()
        
        # Click the button to trigger the prompt dialog
        js_alerts_page.click_js_prompt_button()
        
        # Enter text into the prompt (which should be ignored when dismissed)
        js_alerts_page.enter_prompt_text("This text will be ignored")
        
        # Dismiss the prompt
        js_alerts_page.dismiss_alert()
        
        # Verify the result text
        result_text = js_alerts_page.get_result_text()
        assert "You entered: null" in result_text, \
            f"Expected 'You entered: null' but got '{result_text}'"