from django.db import models
from developer.models import MainCategory
import uuid
from cloudinary.models import CloudinaryField
import cloudinary.uploader
from playwright.sync_api import sync_playwright
import time
# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.OneToOneField(Login, on_delete=models.CASCADE)  # Link to Login model
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    pin_code = models.IntegerField()  # Specific for agent
    email = models.EmailField(max_length=50)
    is_agent = models.BooleanField(default=False)  # Flag to determine if the user is an agent
    messages = models.ManyToManyField('Inbox', related_name='agents', blank=True)  # Messages related to the user
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.login.username


class AgentHouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    AVAILABLE = 'Available'
    SOLD = 'Sold'
    HOUSE_STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (SOLD, 'Sold'),
    ]
    MALE = 'male'
    FEMALE = 'female'
    MIXED = 'mixed'
    HOUSE_GENDER_CHOICES = [
        (MALE, 'male'),
        (FEMALE, 'female'),
        (MIXED, 'mixed'),
    ]
    Caption = models.CharField(max_length=100)
    category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    total_land = models.CharField(max_length=50, null=True, blank=True)
    house_area = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    address = models.TextField(max_length=500)
    description = models.TextField(max_length=500)
    furnished = models.BooleanField(default=False, verbose_name="Is Furnished?")
    land_mark = models.TextField(max_length=100)
    Bedroom = models.CharField(max_length=10)
    Bathroom = models.CharField(max_length=10)
    Kitchen = models.BooleanField(default=False)
    allowed_persons = models.IntegerField(blank=True, null=True, verbose_name="Allowed Persons")
    sequrity_deposit = models.CharField(max_length=50, null=True, blank=True)
    Time_perioud = models.CharField(max_length=50, blank=True, verbose_name="Time Period")
    gender = models.CharField(max_length=50, choices=HOUSE_GENDER_CHOICES, default=MALE)
    location = models.TextField(max_length=200, null=True, blank=True)
    agent_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, blank=True, null=True)  # Storing the phone contact as CharField
    status = models.CharField(max_length=10, choices=HOUSE_STATUS_CHOICES, default=AVAILABLE)
    disabled = models.BooleanField(default=False, verbose_name="Is Disabled?")
    image = CloudinaryField('image', folder="agenthouses") 
    screenshot = CloudinaryField('image', folder="screenshot", null=True, blank= True) 

    def __str__(self):
        return f"{self.Caption} - {self.agent_name}"

    def take_screenshot(self):
        """Captures a screenshot of the specific property card using Playwright"""
        listing_url = "https://buysel.in/properties "  # Your website URL
        screenshot_path = f"/tmp/{self.id}.png"  # Temporary storage

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(listing_url, wait_until="load")

            # Give the page some time to fully render
            time.sleep(2)

            # Selector for the card (Make sure the template has data-house-id="{{ i.id }}")
            card_selector = f"div[data-agenthouse-id='{self.id}']"

            # Debugging - Check if the element is found
            elements = page.locator(card_selector).count()
            print(f"Found {elements} elements with selector {card_selector}")

            if elements > 0:
                page.locator(card_selector).screenshot(path=screenshot_path)
            else:
                print(f"Element not found: {card_selector}, taking full page screenshot instead.")
                page.screenshot(path=screenshot_path, full_page=True)

            browser.close()

        return screenshot_path

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the House instance first

        try:
            screenshot_path = self.take_screenshot()

            # Upload screenshot to Cloudinary
            uploaded_image = cloudinary.uploader.upload(screenshot_path, folder="screenshots")
            self.screenshot = uploaded_image['url']

            super().save(update_fields=['screenshot'])  # Save only the screenshot field
        except Exception as e:
            print(f"Error taking screenshot: {e}")




class AgentLand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    AVAILABLE = 'Available'
    SOLD = 'Sold'
    HOUSE_STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (SOLD, 'Sold'),
    ]
    Caption = models.CharField(max_length=100)
    category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    total_land = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50) 
    space_area = models.CharField(max_length=50)
    address = models.TextField(max_length=500)
    description = models.TextField(max_length=500)
    furnished = models.BooleanField(default=False)
    land_mark = models.TextField(max_length=100)
    sequrity_deposit = models.CharField(max_length=50, null=True, blank=True)
    Time_perioud = models.CharField(max_length=50, blank=True, verbose_name="Time Period")
    location = models.TextField(max_length=200, null=True, blank=True)
    agent_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=HOUSE_STATUS_CHOICES, default=AVAILABLE)
    disabled = models.BooleanField(default=False, verbose_name="Is Disabled?")
    image = CloudinaryField('image', folder="agentlands") 
    screenshot = CloudinaryField('image', folder="screenshot", null=True, blank= True) 

    def __str__(self):
        return f"{self.Caption} - {self.agent_name}"
    
    def take_screenshot(self):
        """Captures a screenshot of the specific property card using Playwright"""
        listing_url = "https://buysel.in/properties "  # Your website URL
        screenshot_path = f"/tmp/{self.id}.png"  # Temporary storage

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(listing_url, wait_until="load")

            # Give the page some time to fully render
            time.sleep(2)

            # Selector for the card (Make sure the template has data-house-id="{{ i.id }}")
            card_selector = f"div[data-agentland-id='{self.id}']"

            # Debugging - Check if the element is found
            elements = page.locator(card_selector).count()
            print(f"Found {elements} elements with selector {card_selector}")

            if elements > 0:
                page.locator(card_selector).screenshot(path=screenshot_path)
            else:
                print(f"Element not found: {card_selector}, taking full page screenshot instead.")
                page.screenshot(path=screenshot_path, full_page=True)

            browser.close()

        return screenshot_path

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the House instance first

        try:
            screenshot_path = self.take_screenshot()

            # Upload screenshot to Cloudinary
            uploaded_image = cloudinary.uploader.upload(screenshot_path, folder="screenshots")
            self.screenshot = uploaded_image['url']

            super().save(update_fields=['screenshot'])  # Save only the screenshot field
        except Exception as e:
            print(f"Error taking screenshot: {e}")

class AgentCommercial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    AVAILABLE = 'Available'
    SOLD = 'Sold'
    HOUSE_STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (SOLD, 'Sold'),
    ]
    Caption = models.CharField(max_length=100)
    category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    total_land = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50)
    address = models.TextField(max_length=500)
    description = models.TextField(max_length=500)
    land_mark = models.TextField(max_length=100)
    sequrity_deposit = models.CharField(max_length=50, null=True, blank=True)
    Time_perioud = models.CharField(max_length=50, blank=True, verbose_name="Time Period")
    location = models.TextField(max_length=200, null=True, blank=True)
    agent_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=10, choices=HOUSE_STATUS_CHOICES, default=AVAILABLE)
    disabled = models.BooleanField(default=False, verbose_name="Is Disabled?")
    amenities = models.TextField(max_length=500)
    image = CloudinaryField('image', folder="agentcommercial") 
    screenshot = CloudinaryField('image', folder="screenshot", null=True, blank= True) 
    def __str__(self):
        return f"{self.Caption} - {self.agent_name}"


    def take_screenshot(self):
        """Captures a screenshot of the specific property card using Playwright"""
        listing_url = "https://buysel.in/properties "  # Your website URL
        screenshot_path = f"/tmp/{self.id}.png"  # Temporary storage

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(listing_url, wait_until="load")

            # Give the page some time to fully render
            time.sleep(2)

            # Selector for the card (Make sure the template has data-house-id="{{ i.id }}")
            card_selector = f"div[data-agentcom-id='{self.id}']"

            # Debugging - Check if the element is found
            elements = page.locator(card_selector).count()
            print(f"Found {elements} elements with selector {card_selector}")

            if elements > 0:
                page.locator(card_selector).screenshot(path=screenshot_path)
            else:
                print(f"Element not found: {card_selector}, taking full page screenshot instead.")
                page.screenshot(path=screenshot_path, full_page=True)

            browser.close()

        return screenshot_path

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the House instance first

        try:
            screenshot_path = self.take_screenshot()

            # Upload screenshot to Cloudinary
            uploaded_image = cloudinary.uploader.upload(screenshot_path, folder="screenshots")
            self.screenshot = uploaded_image['url']

            super().save(update_fields=['screenshot'])  # Save only the screenshot field
        except Exception as e:
            print(f"Error taking screenshot: {e}")


class AgentOffPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    AVAILABLE = 'Available'
    SOLD = 'Sold'
    HOUSE_STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (SOLD, 'Sold'),
    ]
    
    Caption = models.CharField(max_length=100)
    category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    total_land = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50)
    address = models.TextField(max_length=500)
    description = models.TextField(max_length=500)
    rooms = models.CharField(max_length=10)
    land_mark = models.TextField(max_length=100)
    location = models.TextField(max_length=200, null=True, blank=True)
    agent_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=10, choices=HOUSE_STATUS_CHOICES, default=AVAILABLE)
    disabled = models.BooleanField(default=False, verbose_name="Is Disabled?")
    image = CloudinaryField('image', folder="agentoffplan") 
    screenshot = CloudinaryField('image', folder="screenshot", null=True, blank= True) 
    
    def __str__(self):
        return f"{self.Caption} - {self.agent_name}"



    def take_screenshot(self):
        """Captures a screenshot of the specific property card using Playwright"""
        listing_url = "https://buysel.in/properties "  # Your website URL
        screenshot_path = f"/tmp/{self.id}.png"  # Temporary storage

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(listing_url, wait_until="load")

            # Give the page some time to fully render
            time.sleep(2)

            # Selector for the card (Make sure the template has data-house-id="{{ i.id }}")
            card_selector = f"div[data-agentoffplan-id='{self.id}']"

            # Debugging - Check if the element is found
            elements = page.locator(card_selector).count()
            print(f"Found {elements} elements with selector {card_selector}")

            if elements > 0:
                page.locator(card_selector).screenshot(path=screenshot_path)
            else:
                print(f"Element not found: {card_selector}, taking full page screenshot instead.")
                page.screenshot(path=screenshot_path, full_page=True)

            browser.close()

        return screenshot_path

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the House instance first

        try:
            screenshot_path = self.take_screenshot()

            # Upload screenshot to Cloudinary
            uploaded_image = cloudinary.uploader.upload(screenshot_path, folder="screenshots")
            self.screenshot = uploaded_image['url']

            super().save(update_fields=['screenshot'])  # Save only the screenshot field
        except Exception as e:
            print(f"Error taking screenshot: {e}")

class AgentHouseImage(models.Model):
    house = models.ForeignKey(AgentHouse, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder="agenthouses") 

    def __str__(self):
        return f"Image for {self.house.Caption}"
    
class AgentLandImage(models.Model):
    land = models.ForeignKey(AgentLand, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder="agentlands")

    def __str__(self):
        return f"Image for {self.land.Caption}"
   
class AgentCommercialImage(models.Model):
    com = models.ForeignKey(AgentCommercial, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder="agentcommercial")

    def __str__(self):
        return f"Image for {self.com.Caption}"
   
class AgentOffPlanImage(models.Model):
    offplan = models.ForeignKey(AgentOffPlan, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder="agentoffplan")
    def __str__(self):
        return f"Image for {self.offplan.Caption}"


class Inbox(models.Model):
    name = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    messages_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  #
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return f"Enquiry from {self.messages_text}"
    
class AgentProperty(models.Model):
    TYPE_CHOICES = (
        ('house', 'House'),
        ('land', 'Land'),
        ('commercial', 'Commercial'),
        ('offplan', 'OffPlan'),
    )
    id = models.AutoField(primary_key=True)
    type = models.CharField(choices=TYPE_CHOICES, max_length=20)
    caption = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)