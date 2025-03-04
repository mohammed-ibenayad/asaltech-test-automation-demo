from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from automation_framework.src.web.pages.base_page import BasePage

class IFramePage(BasePage):
    # Locators
    IFRAME = (By.ID, "mce_0_ifr")
    EDITOR_BODY = (By.ID, "tinymce")
    BOLD_BUTTON = (By.CSS_SELECTOR, "button[title='Bold']")
    
    def navigate(self):
        """Navigate to the iFrame page"""
        self.driver.get("https://the-internet.herokuapp.com/iframe")
    
    def switch_to_iframe(self):
        """Switch to the iFrame containing the editor"""
        iframe = self.find_element(self.IFRAME)
        self.driver.switch_to.frame(iframe)
    
    def switch_to_main_content(self):
        """Switch back to the main page content"""
        self.driver.switch_to.default_content()
    
    def get_editor_text(self):
        """Get the text from the editor
        
        Returns:
            str: The text in the editor
        """
        self.switch_to_iframe()
        text = self.get_text(self.EDITOR_BODY)
        self.switch_to_main_content()
        return text
    
    def clear_editor(self):
        """Clear all text from the editor"""
        self.switch_to_iframe()
        editor = self.find_element(self.EDITOR_BODY)
        editor.clear()
        self.switch_to_main_content()
    
    def type_text(self, text):
        """Type text into the editor
        
        Args:
            text (str): The text to type
        """
        self.switch_to_iframe()
        editor = self.find_element(self.EDITOR_BODY)
        editor.send_keys(text)
        self.switch_to_main_content()
    
    def format_bold(self):
        """Click the Bold button in the toolbar to format selected text"""
        # Need to be in main content to access the toolbar
        self.switch_to_main_content()
        self.click(self.BOLD_BUTTON)
    
    def select_all_text(self):
        """Select all text in the editor using keyboard shortcut"""
        self.switch_to_iframe()
        editor = self.find_element(self.EDITOR_BODY)
        # Use Ctrl+A to select all text
        if self.driver.name == 'safari':
            # For Safari, use Command+A
            editor.send_keys(Keys.COMMAND, 'a')
        else:
            # For other browsers, use Control+A
            editor.send_keys(Keys.CONTROL, 'a')
        self.switch_to_main_content()