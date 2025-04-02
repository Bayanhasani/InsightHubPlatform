from django.db import models
from account import models
from django.db import models
from account.models import CustomUser  # استيراد CustomUser
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="customer_profile")
    company_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    def _str_(self):
        return self.company_name
