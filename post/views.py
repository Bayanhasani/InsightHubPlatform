from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post

# عرض صفحة المنشورات (عرض النموذج وإضافة منشور جديد)
def post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)  # حفظ المنشور بدون تطبيق التغييرات بعد
            post.user = request.user  # ربط المنشور بالمستخدم الحالي
            post.save()  # حفظ المنشور في قاعدة البيانات
            return redirect('post_view')  # إعادة التوجيه بعد الحفظ (إلى نفس الصفحة لعرض المنشور)

    else:
        form = PostForm()  # عرض النموذج الفارغ عند طلب الصفحة لأول مرة

    # الحصول على المنشورات العادية والوظيفية
    general_posts = Post.objects.filter(post_type='general').order_by('-created_at')
    job_posts = Post.objects.filter(post_type='job').order_by('-created_at')

    return render(request, "post/post.html", {
        'form': form,
        'general_posts': general_posts,  # عرض المنشورات العادية
        'job_posts': job_posts,  # عرض المنشورات الوظيفية
    })