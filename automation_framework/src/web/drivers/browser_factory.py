from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class BrowserFactory:
    @staticmethod
    def get_browser(browser_type="chrome", headless=False):
        if browser_type.lower() == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        elif browser_type.lower() == "firefox":
            # Similar setup for Firefox
            pass
        # Add other browsers as needed
        
        driver.maximize_window()
        return driver