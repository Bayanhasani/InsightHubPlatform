from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('graduate', 'Graduate'),
        ('student', 'Student'),
        ('company', 'Company'),
    ]
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    def save(self):
        if self.pk:  # Only for existing users
            old_status = CustomUser.objects.get(pk=self.pk).is_verified
            if self.is_verified != old_status:
                Verification.objects.filter(user=self).update(
                    status='approved' if self.is_verified else 'rejected'
                )
        super().save()


class Verification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    verification_type = models.CharField(max_length=10, choices=CustomUser.USER_TYPES)
    university_id = models.CharField(max_length=20, blank=True, null=True)
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)
    request_message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'),
                                                       ('approved', 'Approved'), 
                                                       ('rejected', 'Rejected')],
                                                         default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def save(self):
        if self.status == 'approved':
            self.user.is_verified = True
            self.user.save()
        elif self.status == 'rejected':
            self.user.is_verified = False
            self.user.save()
        super().save()  # Save the Verification record
    
    
    def __str__(self):
        return f"{self.user.username} - {self.verification_type} ({self.status})"
