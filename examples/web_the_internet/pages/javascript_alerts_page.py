from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from automation_framework.src.web.pages.base_page import BasePage

class JavaScriptAlertsPage(BasePage):
    # Locators
    JS_ALERT_BUTTON = (By.XPATH, "//button[contains(text(), 'Click for JS Alert')]")
    JS_CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(), 'Click for JS Confirm')]")
    JS_PROMPT_BUTTON = (By.XPATH, "//button[contains(text(), 'Click for JS Prompt')]")
    RESULT_TEXT = (By.ID, "result")
    
    def navigate(self):
        """Navigate to the JavaScript Alerts page"""
        self.driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    
    def click_js_alert_button(self):
        """Click the button that triggers a JavaScript alert"""
        self.click(self.JS_ALERT_BUTTON)
    
    def click_js_confirm_button(self):
        """Click the button that triggers a JavaScript confirm dialog"""
        self.click(self.JS_CONFIRM_BUTTON)
    
    def click_js_prompt_button(self):
        """Click the button that triggers a JavaScript prompt dialog"""
        self.click(self.JS_PROMPT_BUTTON)
    
    def accept_alert(self):
        """Accept the currently displayed alert/confirm/prompt"""
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()
    
    def dismiss_alert(self):
        """Dismiss (cancel) the currently displayed confirm/prompt"""
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.dismiss()
    
    def get_alert_text(self):
        """Get the text from the currently displayed alert/confirm/prompt
        
        Returns:
            str: The text displayed in the alert
        """
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        return alert.text
    
    def enter_prompt_text(self, text):
        """Enter text into a JavaScript prompt dialog
        
        Args:
            text (str): The text to enter into the prompt
        """
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.send_keys(text)
    
    def get_result_text(self):
        """Get the text from the result element
        
        Returns:
            str: The text from the result element
        """
        return self.get_text(self.RESULT_TEXT)