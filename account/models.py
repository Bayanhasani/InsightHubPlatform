from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from uuid import uuid4
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('graduate', 'Graduate'),
        ('student', 'Student'),
        ('company', 'Company'),
    ]
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    is_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)

    def generate_verification_token(self):
        self.verification_token = str(uuid4())  # Random unique token
        self.token_expiry = timezone.now() + timedelta(hours=12)  # Expires in 24h
        self.save()
        return self.verification_token
    
    def clean(self):
        if self.user_type == 'student' and not self.email.endswith('@mutah.edu.jo'):
            raise ValidationError("Students must register with a @mutah.edu.jo email.")
        
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.pk:  # Only for existing users
            old_status = CustomUser.objects.get(pk=self.pk).is_verified
            if self.is_verified != old_status:
                Verification.objects.filter(user=self).update(
                    status='approved' if self.is_verified else 'rejected'
                )
        self.clean()
        super().save(*args,**kwargs)


class Verification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    verification_type = models.CharField(max_length=10, choices=CustomUser.USER_TYPES)
    university_id = models.CharField(max_length=20, blank=True, null=True)
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)
    request_message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'),
                                                       ('approved', 'Approved'), 
                                                       ('rejected', 'Rejected')],
                                                         default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.user.user_type == 'student':
            return  
        if self.status == 'approved':
            self.user.is_verified = True
            self.user.save()
        elif self.status == 'rejected':
            self.user.is_verified = False
            self.user.save()
        super().save( *args, **kwargs)  # Save the Verification record
    
    
    def __str__(self):
        return f"{self.user.username} - {self.verification_type} ({self.status})"






class Profile(models.Model):
    location_choices={"Amman":"Amman",
              "karak":"AlKarak",
              "Zarqa":"Zarqa",
              "Irbid":"Irbid",
              "Aqaba":"Aqaba",
              "Mafraq":"Mafraq",
              "Madaba":"Madaba",
              "Al-Balqa":"Al-Balqa",
              "Jerash":"Jerash",
              "Ma'an":"Ma'an",
              "Ajloun":"Ajloun",
              "Tafilah":"Tafilah"}
    
    major_choices={"cis":"CIS",
                   "AI":"AI",
                   "software engineering":"software engineering",
                   "Cyber Security":"Cyber Security"}
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    display_name = models.CharField(max_length=150, blank=True, 
                                  help_text="How you want your name displayed publicly")
    
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True,default='profile_pics/default_profile.jpg')
    phone_number = PhoneNumberField(blank=True, help_text="Enter your phone number")
    location = models.CharField(max_length=100, blank=True,choices=location_choices)
    
    # Common social links
    github = models.URLField(blank=True)
    
    
    # Graduate-specific fields
    current_job_title = models.CharField(max_length=100, blank=True, null=True)
    current_company = models.CharField(max_length=100, blank=True, null=True)
    work_experience = models.TextField(blank=True, null=True)
    # Graduate-student fields 
    major = models.CharField(max_length=100, blank=True, null=True,choices=major_choices)
    graduation_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1995),
            MaxValueValidator( timezone.now().year + 5)  # Allows up to 5 years in future
        ]
    )    
    skills = models.TextField(blank=True, null=True)

    # Company-specific fields
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    company_size = models.CharField(max_length=50, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    founded_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(timezone.now().year)  # Can't be in future
        ]
    )    
    #-----------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_full_name(self):
        """Returns the properly formatted name based on user type"""
        if self.user.user_type in ['student', 'graduate']:
            if self.first_name and self.last_name:
                return f"{self.first_name} {self.last_name}"
            return self.user.get_full_name() or self.user.username
        elif self.user.user_type == 'company':
            return self.company_name or self.user.username
        return self.user.username
    
    def get_display_fields(self):
        """Returns fields relevant to the user's type"""
        fields = {
            'common': {
                'Bio': self.bio,
                'Location': self.location,
                'Phone': self.phone_number,
            },
            'social': {
                'GitHub': self.github,
            }
        }
        
        if self.user.user_type == 'student':

         if self.user.user_type == 'graduate':
            fields['user information'] = {
                'Current Job Title': self.current_job_title,
                'Current Company': self.current_company,
                'Work Experience': self.work_experience,
            }
        elif self.user.user_type == 'company':
            fields['user information'] = {
                'Company Name': self.company_name,
                'Description': self.company_description,
                'Company Size': self.company_size,
                'Industry': self.industry,
                'Founded Year': self.founded_year,
            }
        if self.user.user_type in ['student', 'graduate'] and self.skills:
            fields['user information'] = { 
                'Skills': self.skills,
                'Major': self.major,
                'Graduation Year': self.graduation_year,
            }
            
        return fields