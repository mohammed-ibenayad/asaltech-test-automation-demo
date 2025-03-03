from selenium.webdriver.common.by import By
from automation_framework.src.web.pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".flash.success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".flash.error")
    
    def navigate(self):
        self.driver.get("https://the-internet.herokuapp.com/login")
    
    def login(self, username, password):
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
    
    def is_login_successful(self):
        # Return True/False instead of the WebElement
        return self.is_element_visible(self.SUCCESS_MESSAGE) is not False
    
    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)