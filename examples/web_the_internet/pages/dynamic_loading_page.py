from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from automation_framework.src.web.pages.base_page import BasePage

class DynamicLoadingPage(BasePage):
    # Locators
    START_BUTTON = (By.CSS_SELECTOR, "#start button")
    LOADING_INDICATOR = (By.ID, "loading")
    FINISH_TEXT = (By.ID, "finish")
    
    def navigate_to_example(self, example_number):
        """Navigate to a specific dynamic loading example.
        
        Args:
            example_number (int): Example number (1 or 2)
        """
        self.driver.get(f"https://the-internet.herokuapp.com/dynamic_loading/{example_number}")
    
    def click_start(self):
        """Click the start button to trigger the loading."""
        self.click(self.START_BUTTON)
    
    def wait_for_loading_to_complete(self, timeout=10):
        """Wait for the loading indicator to disappear and finish element to appear.
        
        Args:
            timeout (int): Maximum wait time in seconds
        """
        try:
            # Wait for loading indicator to appear first (to ensure we don't miss it)
            WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located(self.LOADING_INDICATOR)
            )
        except:
            # In case we missed the loading indicator, continue
            pass
        
        # Then wait for it to disappear
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(self.LOADING_INDICATOR)
        )
        
        # Finally, wait for the finish element to be visible
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.FINISH_TEXT)
        )
    
    def get_finish_text(self):
        """Get the text from the finish element.
        
        Returns:
            str: Text of the finish element
        """
        try:
            # Wait for the element to be visible first to ensure it's loaded
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.FINISH_TEXT)
            )
            return element.text
        except Exception as e:
            # Log the error for debugging
            print(f"Error getting finish text: {e}")
            return ""
    
    def is_finish_element_displayed(self):
        """Check if the finish element is displayed.
        
        Returns:
            bool: True if displayed, False otherwise
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(self.FINISH_TEXT)).is_displayed()
        except:
            return False