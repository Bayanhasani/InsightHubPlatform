from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'get_post_type_display', 'created_at', 'is_published')
    list_filter = ('post_type', 'is_published')
    search_fields = ('content', 'author__username')