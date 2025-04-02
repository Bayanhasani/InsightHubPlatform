from django import forms
from .models import Verification
from django.contrib.auth import get_user_model

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
    class Meta:
        model = Verification
        fields = ['certificate']

class CompanyVerificationForm(forms.ModelForm):
    class Meta:
        model = Verification
        fields = ['request_message']