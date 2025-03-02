from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.core.os_manager import ChromeType
import logging
import os

# Enable detailed logging for webdriver-manager
os.environ['WDM_LOG'] = str(logging.INFO)
# Optionally disable SSL verification if you have issues with SSL certificates
# os.environ['WDM_SSL_VERIFY'] = '0'

class BrowserFactory:
    @staticmethod
    def get_browser(browser_type="chrome", headless=False):
        """
        Factory method to get a WebDriver instance based on browser type.
        
        Args:
            browser_type (str): Type of browser ('chrome', 'firefox', 'edge', 'ie', 'opera', 'chromium', 'brave')
            headless (bool): Whether to run the browser in headless mode
            
        Returns:
            WebDriver: Configured WebDriver instance
            
        Raises:
            ValueError: If browser_type is not supported
        """
        browser_type = browser_type.lower()
        
        if browser_type == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
            
        elif browser_type == "chromium":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
                
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                options=options
            )
            
        elif browser_type == "brave":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
                
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()),
                options=options
            )
            
        elif browser_type == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
            
        elif browser_type == "edge":
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument("--headless")
            
            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=options
            )
            
        elif browser_type == "ie":
            options = webdriver.IeOptions()
            
            driver = webdriver.Ie(
                service=IEService(IEDriverManager().install()),
                options=options
            )
            
        elif browser_type == "opera":
            # Opera setup is different as it uses Remote WebDriver
            from selenium.webdriver.chrome import service as chrome_service_module
            
            opera_service = chrome_service_module.Service(OperaDriverManager().install())
            opera_service.start()
            
            options = webdriver.ChromeOptions()
            options.add_experimental_option('w3c', True)
            
            # If Opera is installed in non-standard location, uncomment and set the path:
            # options.binary_location = "path/to/opera.exe"
            
            driver = webdriver.Remote(
                opera_service.service_url, 
                options=options
            )
            
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
        
        # Common setup for all browsers
        if browser_type != "opera":  # Opera Remote WebDriver handles window differently
            driver.maximize_window()
        return driver