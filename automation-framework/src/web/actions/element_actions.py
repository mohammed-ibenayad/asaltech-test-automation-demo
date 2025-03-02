from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class ElementActions:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)
    
    def hover(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.actions.move_to_element(element).perform()
    
    def drag_and_drop(self, source_locator, target_locator):
        source = self.wait.until(EC.presence_of_element_located(source_locator))
        target = self.wait.until(EC.presence_of_element_located(target_locator))
        self.actions.drag_and_drop(source, target).perform()
    
    # Add more advanced element interactions