# import requests
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.files.base import ContentFile
# import base64
# from .models import House, Land, Commercial, OffPlan
# from agents.models import AgentHouse, AgentLand, AgentCommercial, AgentOffPlan

# MODEL_MAPPING = {
#     'model1': House,
#     'model2': Land,
#     'model3': Commercial,
#     'model4': OffPlan,
#     'model5': AgentHouse,
#     'model6': AgentLand,
#     'model7': AgentCommercial,
#     'model8': AgentOffPlan,
    
# }


# @receiver(post_save, sender=House)
# @receiver(post_save, sender=Land)
# @receiver(post_save, sender=Commercial)
# @receiver(post_save, sender=OffPlan)
# @receiver(post_save, sender=AgentHouse)
# @receiver(post_save, sender=AgentLand)
# @receiver(post_save, sender=AgentCommercial)
# @receiver(post_save, sender=AgentOffPlan)
# def capture_screenshot(sender, instance, created, **kwargs):
#     """Automatically capture screenshot when a model instance is saved."""
#     if created:  # Only when a new instance is created
#         url = "http://127.0.0.1:8000/save-screenshot/"  # Update with your actual API URL
        
#         data = {
#             "model_name": sender.__name__.lower(),  # Convert model name to lowercase
#             "object_id": str(instance.id)
#         }

#         response = requests.post(url, json=data)

#         if response.status_code == 200:
#             print(f"✅ Screenshot saved successfully for {sender.__name__} - {instance.id}")
#         else:
#             print(f"❌ Failed to save screenshot for {sender.__name__}: {response.text}")
