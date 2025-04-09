from django import forms
from .models import Verification
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()  # Get the custom user model
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,label="Password")
    password2 = forms.CharField( widget=forms.PasswordInput,label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'user_type', 'email', 'password'] 

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        user_type = cleaned_data.get('user_type')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        # Validate university email for students
        if user_type == 'student' and not email.endswith('@mutah.edu.jo'):
            raise forms.ValidationError(
                "Students must register with a @mutah.edu.jo email."
            )

        # Validate password match
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user  


class GraduateVerificationForm(forms.ModelForm):
    certificate = forms.FileField(
        label="Graduation Certificate",
        required=True,
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.png'})
    )
    
    class Meta:
        model = Verification
        fields = ['certificate']

    def clean_certificate(self):
        certificate = self.cleaned_data.get('certificate')
        if not certificate:
            raise ValidationError("Graduation certificate is required")
        return certificate

class CompanyVerificationForm(forms.ModelForm):
    request_message = forms.CharField(
        label="Verification Request Details",
        required=True,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Please explain your connection to the university"
    )
    class Meta:
        model = Verification
        fields = ['request_message']

    def clean_request_message(self):
        message = self.cleaned_data.get('request_message')
        if not message or len(message.strip()) < 50:
            raise ValidationError("Please provide at least 50 characters of explanation")
        return message.strip()