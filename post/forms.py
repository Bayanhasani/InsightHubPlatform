from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'content', 'image', 'job_title', 'job_company', 'job_location']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show job fields only when post type is job
        if self.instance.post_type != 'job' or 'post_type' in self.data:
            for field in ['job_title', 'job_company', 'job_location']:
                self.fields[field].required = False     # not required if the post not job post 