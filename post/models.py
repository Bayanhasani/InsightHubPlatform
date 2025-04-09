from django.db import models
from account.models import CustomUser
from django.urls import reverse

class Post(models.Model):
    POST_TYPES = [
        ('job', 'Job Post'),
        ('general', 'General Post'),
        ('question', 'Question Post')
    ]
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts',null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    
    # For job posts only
    job_title = models.CharField(max_length=100, blank=True)
    job_company = models.CharField(max_length=100, blank=True)
    job_location = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_post_type_display()} by {self.author.username}"
    
    def get_absolute_url(self):     # Generates URL for individual post details.
        return reverse('post_detail', args=[str(self.id)])