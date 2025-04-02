from django.db import models
from account import models
# Create your models here.
class CompanyProfile(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم الشركة")
    description = models.TextField(blank=True, null=True, verbose_name="وصف الشركة")
    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    address = models.CharField(max_length=255, verbose_name="العنوان")
    website = models.URLField(blank=True, null=True, verbose_name="الموقع الإلكتروني")
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name="شعار الشركة")

    def _str_(self):
        return self.name 