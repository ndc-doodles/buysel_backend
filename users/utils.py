# users/utils.py
from playwright.sync_api import sync_playwright
from cloudinary.uploader import upload
import tempfile

def capture_screenshot_and_upload(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launching browser in headless mode
        page = browser.new_page()  # Create a new page
        page.goto(url)  # Navigating to the provided URL
        screenshot = page.screenshot()  # Taking a screenshot of the page
        browser.close()  # Closing the browser

    # Saving the screenshot to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        tmpfile.write(screenshot)  # Writing the screenshot to the temporary file
        tmpfile.close()

        # Uploading the screenshot to Cloudinary and returning the URL
        response = upload(tmpfile.name, folder="houses/screenshot")
        return response['secure_url']  # The URL to the uploaded image
