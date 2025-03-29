from django import forms
from .models import Post

# نموذج المنشور (لجميع أنواع المنشورات)
class PostForm(forms.ModelForm):
    job_title = forms.CharField(max_length=255, required=False, label="Job Title")
    company_name = forms.CharField(max_length=255, required=False, label="Company Name")
    job_description = forms.CharField(widget=forms.Textarea, required=False, label="Job Description")
    job_file = forms.FileField(required=False, label="Attach File (Optional)")

    class Meta:
        model = Post
        fields = ['content', 'image', 'post_type']  # الحقول التي ستظهر في النموذج: المحتوى، الصورة، نوع المنشور

    def clean(self):
        """التحقق من الحقول إذا كان المنشور من نوع وظيفة."""
        cleaned_data = super().clean()  # الحصول على البيانات المدخلة
        post_type = cleaned_data.get('post_type')  # تحديد نوع المنشور

        # إذا كان المنشور من نوع "وظيفة"، تأكد من إدخال جميع التفاصيل الخاصة بالوظيفة
        if post_type == 'job':
            if not cleaned_data.get('job_title'):
                raise forms.ValidationError("يجب إدخال المسمى الوظيفي.")
            if not cleaned_data.get('company_name'):
                raise forms.ValidationError("يجب إدخال اسم الشركة.")
            if not cleaned_data.get('job_description'):
                raise forms.ValidationError("يجب إدخال وصف الوظيفة.")
        
        return cleaned_data  # إرجاع البيانات بعد التحقق