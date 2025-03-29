from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

 
    POST_TYPE_CHOICES = [
        ('general', 'General Post'),
        ('job', 'Job Post'),
    ]
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='general')

    def is_job_post(self):
        return self.post_type == 'job'

    def _str_(self):
        return f"Post by {self.user.username} ({self.get_post_type_display()})"