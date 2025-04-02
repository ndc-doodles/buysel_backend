from django.db import models
import uuid
from cloudinary.models import CloudinaryField
import cloudinary.uploader
from playwright.sync_api import sync_playwright
import time
# Create your models here.
class MainCategory(models.Model):
    SALE = 'Sale'
    RENT = 'Rent'
    RESELL = 'Resell'
    LEASE = 'Lease'
    CATEGORY_CHOICES = [
        (SALE, 'Sale'),
        (RENT, 'Rent'),
        (RESELL, 'Resell'),
        (LEASE, 'Lease'),
    ]

    catgory = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return self.catgory


class House(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    AVAILABLE = 'Available'
    SOLD = 'Sold'
    HOUSE_STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (SOLD, 'Sold'),
    ]
    MALE = 'male'
    FEMALE = 'female'
    MIXED = 'mixed'
    HOUSE_GENDER_CHOICES =[ 
        (MALE ,'male'),
        (FEMALE, 'female'),
        (MIXED, 'mixed'),
    ]
    Caption = models.CharField(max_length=100)
    category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)
    total_land = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50)
    house_area = models.CharField(max_length=50)
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
    username = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=HOUSE_STATUS_CHOICES, default=AVAILABLE)
    disabled = models.BooleanField(default=False, verbose_name="Is Disabled?")
    image = CloudinaryField('image', folder="houses") 
    screenshot = CloudinaryField('image', folder="screenshot", null=True, blank= True) 
    def __str__(self):
        return f"{self.Caption} - {self.username}"
    

    def take_screenshot(self):
        """Captures a screenshot of the specific property card using Playwright"""
        listing_url = "http://127.0.0.1:8000/properties "  # Your website URL
        screenshot_path = f"/tmp/{self.id}.png"  # Temporary storage

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(listing_url, wait_until="load")

            # Give the page some time to fully render
            time.sleep(2)

            # Selector for the card (Make sure the template has data-house-id="{{ i.id }}")
            card_selector = f"div[data-house-id='{self.id}']"

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

class HouseImage(models.Model):
    house = models.ForeignKey(House, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder="houses")   # Multiple images for the house
   
    def __str__(self):
        return f"Image for {self.house.Caption}"  # This will be the main image



class Land(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    username = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=HOUSE_STATUS_CHOICES, default=AVAILABLE)
    disabled = models.BooleanField(default=False)
    image = CloudinaryField('image', folder="lands") 
    screenshot = CloudinaryField('image', folder="screenshot", null=True, blank= True) 

    def __str__(self):
        return f"{self.Caption} - {self.username}"
    

    
    def take_screenshot(self):
        """Captures a screenshot of the specific property card using Playwright"""
        listing_url = "http://127.0.0.1:8000/properties "  # Your website URL
        screenshot_path = f"/tmp/{self.id}.png"  # Temporary storage

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(listing_url, wait_until="load")

            # Give the page some time to fully render
            time.sleep(2)

            # Selector for the card (Make sure the template has data-house-id="{{ i.id }}")
            card_selector = f"div[data-land-id='{self.id}']"

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


class LandImage(models.Model):
    land = models.ForeignKey(Land, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder="lands")   # Multiple images for the house

    def __str__(self):
        return f"Image for {self.land.Caption}"


class Commercial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    username = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=HOUSE_STATUS_CHOICES, default=AVAILABLE)
    disabled = models.BooleanField(default=False)
    amenities = models.TextField(max_length=500)
    image = CloudinaryField('image', folder="commercial") 
    screenshot = CloudinaryField('image', folder="screenshot", null=True, blank= True) 
    def __str__(self):
        return f"{self.Caption} - {self.username}"
    
    
    def take_screenshot(self):
        """Captures a screenshot of the specific property card using Playwright"""
        listing_url = "http://127.0.0.1:8000/properties "  # Your website URL
        screenshot_path = f"/tmp/{self.id}.png"  # Temporary storage

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(listing_url, wait_until="load")

            # Give the page some time to fully render
            time.sleep(2)

            # Selector for the card (Make sure the template has data-house-id="{{ i.id }}")
            card_selector = f"div[data-com-id='{self.id}']"

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


class CommercialImage(models.Model):
    commercial = models.ForeignKey(Commercial, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder="commercial")  # Multiple images for the house

    def __str__(self):
        return f"Image for {self.commercial.Caption}"


class OffPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    username = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=HOUSE_STATUS_CHOICES, default=AVAILABLE)
    disabled = models.BooleanField(default=False)
    image = CloudinaryField('image', folder="offplan")  # This will be the main image
    screenshot = CloudinaryField('image', folder="screenshot", null=True, blank= True) 

    def __str__(self):
        return f"{self.Caption} - {self.username}"

    
    def take_screenshot(self):
        """Captures a screenshot of the specific property card using Playwright"""
        listing_url = "http://127.0.0.1:8000/properties "  # Your website URL
        screenshot_path = f"/tmp/{self.id}.png"  # Temporary storage

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(listing_url, wait_until="load")

            # Give the page some time to fully render
            time.sleep(2)

            # Selector for the card (Make sure the template has data-house-id="{{ i.id }}")
            card_selector = f"div[data-offplan-id='{self.id}']"

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




class OffplanImage(models.Model):
    offplan = models.ForeignKey(OffPlan, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder="offplan") 

    def __str__(self):
        return f"Image for {self.offplan.Caption}"


class AgentForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    address = models.TextField()
    phone_number = models.CharField(max_length=12)
    Dealings = models.CharField(max_length=100)
    image = models.ImageField(upload_to='agent-image')

    def __str__(self):
        return self.name
    
class Propertylist(models.Model):
    property_name =models.CharField(max_length=100)
    locations = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    about_the_property = models.TextField()
    image = models.ImageField(upload_to='property-image')

    def __str__(self):
        return self.property_name

# class ItemImage(models.Model):
#     house = models.ForeignKey('House', null=True, blank=True, on_delete=models.CASCADE, related_name='images')
#     land = models.ForeignKey('Land', null=True, blank=True, on_delete=models.CASCADE, related_name='images')
#     commercial = models.ForeignKey('Commercial', null=True, blank=True, on_delete=models.CASCADE, related_name='images')
#     offplan = models.ForeignKey('OffPlan', null=True, blank=True, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='item-images/')

#     def __str__(self):
#         return f"Image for {self.house or self.land or self.commercial or self.offplan}"

class Blog(models.Model):
    blog_head = models.CharField(max_length=100)
    modal_head = models.CharField(max_length=100)
    date = models.DateField()
    card_paragraph = models.TextField()
    modal_paragraph = models.TextField()
    image = models.ImageField(upload_to='blogs')


    def __str__(self):
        return self.blog_head