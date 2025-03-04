from selenium.webdriver.common.by import By
from automation_framework.src.web.pages.base_page import BasePage

class FileUploadPage(BasePage):
    # Locators
    FILE_UPLOAD_INPUT = (By.ID, "file-upload")
    UPLOAD_BUTTON = (By.ID, "file-submit")
    UPLOAD_SUCCESS_MESSAGE = (By.TAG_NAME, "h3")
    UPLOADED_FILES = (By.ID, "uploaded-files")
    
    def navigate(self):
        """Navigate to the file upload page"""
        self.driver.get("https://the-internet.herokuapp.com/upload")
    
    def upload_file(self, file_path):
        """Upload a file
        
        Args:
            file_path (str): Absolute path to the file to upload
        """
        # Set the file path in the file input
        self.find_element(self.FILE_UPLOAD_INPUT).send_keys(file_path)
        
        # Click the upload button
        self.click(self.UPLOAD_BUTTON)
    
    def get_success_message(self):
        """Get the text of the success message
        
        Returns:
            str: The text of the success message
        """
        return self.get_text(self.UPLOAD_SUCCESS_MESSAGE)
    
    def get_uploaded_filename(self):
        """Get the name of the uploaded file
        
        Returns:
            str: The filename that was uploaded
        """
        return self.get_text(self.UPLOADED_FILES)
    
    def is_upload_successful(self):
        """Check if the upload was successful
        
        Returns:
            bool: True if the upload was successful, False otherwise
        """
        try:
            # Check if the success message is displayed
            success_message = self.get_success_message()
            return "File Uploaded!" in success_message
        except:
            return False