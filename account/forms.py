from django import forms
from .models import Verification
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the custom user model

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Hide password input

    class Meta:
        model = User  # Ensure it uses your CustomUser model
        fields = ['username', 'user_type','email', 'password']
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        user_type = cleaned_data.get('user_type')

        if user_type == 'student' and not email.endswith('@mutah.edu.jo'):
            raise forms.ValidationError(
                "Students must register with a @mutah.edu.jo email."
            )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash password
        if commit:
            user.save()
        return user
    
    


class GraduateVerificationForm(forms.ModelForm):
    class Meta:
        model = Verification
        fields = ['certificate']

class CompanyVerificationForm(forms.ModelForm):
    class Meta:
        model = Verification
        fields = ['request_message']