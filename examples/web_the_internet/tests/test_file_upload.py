import pytest
import os
import tempfile
from automation_framework.src.core.base.web_test_base import WebTestBase
from examples.web_the_internet.pages.file_upload_page import FileUploadPage

class TestFileUpload(WebTestBase):
    
    @pytest.fixture
    def upload_page(self, browser):
        """Fixture to create an instance of the UploadPage"""
        return FileUploadPage(browser)
    
    @pytest.fixture
    def temp_file(self):
        """Fixture to create a temporary file for upload testing"""
        # Create a temporary file
        temp_path = os.path.join(tempfile.gettempdir(), f"upload_test_{os.urandom(8).hex()}.txt")
        
        # Write some content to the file
        with open(temp_path, 'w') as f:
            f.write('This is a test file for upload testing')
        
        # Return the file path
        yield temp_path
        
        # Attempt to clean up the file, but don't fail if we can't
        try:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        except PermissionError:
            print(f"Warning: Could not delete temporary file {temp_path}")
            # The file will be cleaned up by the OS eventually
    
    def test_successful_file_upload(self, upload_page, temp_file):
        """Test that a file can be successfully uploaded"""
        # Navigate to the upload page
        upload_page.navigate()
        
        # Upload the file
        upload_page.upload_file(temp_file)
        
        # Verify upload was successful
        assert upload_page.is_upload_successful(), "File upload should be successful"
        
        # Verify the filename is displayed correctly
        # Extract just the filename from the full path
        expected_filename = os.path.basename(temp_file)
        actual_filename = upload_page.get_uploaded_filename()
        
        assert expected_filename in actual_filename, \
            f"Expected filename '{expected_filename}' to be in '{actual_filename}'"