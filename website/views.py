from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from post.models import Post
from django.core.paginator import Paginator
from django.views.decorators.csrf import ensure_csrf_cookie

@login_required(login_url='login')
def index(request):
    # Get all published posts ordered by newest first
    posts = Post.objects.filter(is_published=True).select_related('author').order_by('-created_at')
    
    # Add pagination (10 posts per page)
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'pages/index.html', {
        'page_obj': page_obj,
        'post_count': paginator.count
    })
def welcome(request):
    return render(request,"pages/welcome.html")


