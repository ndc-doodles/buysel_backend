from playwright.sync_api import sync_playwright
from cloudinary.uploader import upload
import tempfile

def capture_screenshot_and_upload(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch browser in headless mode
        page = browser.new_page()  # Create a new page

        # Navigate to the URL and wait until the network is idle
        page.goto(url, timeout=60000, wait_until="domcontentloaded")  

        screenshot = page.screenshot()  # Take a screenshot of the page
        browser.close()  # Close the browser

    # Save the screenshot to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        tmpfile.write(screenshot)  # Write the screenshot to the temporary file
        tmpfile.close()

        # Upload the screenshot to Cloudinary and return the URL
        response = upload(tmpfile.name, folder="houses/screenshot")
        return response['secure_url']
