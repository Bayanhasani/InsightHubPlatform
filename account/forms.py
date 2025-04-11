from django import forms
from .models import Verification,Profile
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils import timezone
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




class ProfileForm(forms.ModelForm):
    # Common fields with enhanced widgets
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Tell us about yourself...'
        }),
        required=False
    )
    
    phone_number = PhoneNumberField(
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g. +962790123456'
    }),
    required=False,
    help_text="Enter phone number with country code (e.g. +962790123456)"
)
    
    graduation_year = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'min': 1995,
            'max': timezone.now().year + 5,
            'placeholder': 'YYYY'
        }),
        required=False,
        validators=[
            MinValueValidator(1995),
            MaxValueValidator(timezone.now().year + 5)
        ]
    )
    
    founded_year = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'min': 2000,
            'max': timezone.now().year,
            'placeholder': 'YYYY'
        }),
        required=False,
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(timezone.now().year)
        ]
    )
    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'display_name',
            'profile_picture', 'bio', 'phone_number', 'location', 'github',
            'major', 'graduation_year', 'skills','current_job_title',
              'current_company', 'work_experience','company_name', 
              'company_description', 'company_size', 'industry','founded_year'
        ]
        widgets = {
            'location': forms.Select(attrs={'class': 'form-select'}),
            'major': forms.Select(attrs={'class': 'form-select'}),
            'skills': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'List your skills separated by commas'
            }),
            'work_experience': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Describe your work experience...'
            }),
            'company_description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Describe your company...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance.user if self.instance else None
        # Add name fields conditionally
        if user and user.user_type in ['student', 'graduate']:
            self.fields['first_name'] = forms.CharField(
                required=True,
                widget=forms.TextInput(attrs={
                    'placeholder': 'First Name',
                    'class': 'form-control'
                })
            )
            self.fields['last_name'] = forms.CharField(
                required=True,
                widget=forms.TextInput(attrs={
                    'placeholder': 'Last Name',
                    'class': 'form-control'
                })
            )
            self.fields['display_name'] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={
                    'placeholder': 'Preferred Display Name (optional)',
                    'class': 'form-control'
                }),
                help_text="How you want your name to appear publicly"
            )
        else:
            # Remove fields for companies
            self.fields.pop('first_name', None)
            self.fields.pop('last_name', None)
            self.fields.pop('display_name', None)
    
        # Set field requirements based on user type
        if user and user.user_type == 'student':
            self.fields['major'].required = True
        elif user and user.user_type == 'graduate':
            self.fields['current_job_title'].required = True
        elif user and user.user_type == 'company':
            self.fields['company_name'].required = True
            self.fields['company_description'].required = True

        # Add help texts
        self.fields['github'].help_text = "Your GitHub profile URL"
        self.fields['skills'].help_text = "Separate skills with commas (e.g., Python, Django, JavaScript)"
        
       
    def clean_skills(self):
        skills = self.cleaned_data.get('skills', '')
        if skills:
            # Remove empty skills and strip whitespace
            skills_list = [skill.strip() for skill in skills.split(',') if skill.strip()]
            return ', '.join(skills_list)
        return skills

    def clean(self):
        cleaned_data = super().clean()
        user = self.instance.user if self.instance else None
        
        # Validate graduation year for students/graduates
        if user and user.user_type in ['student', 'graduate']:
            graduation_year = cleaned_data.get('graduation_year')
            if graduation_year and graduation_year > timezone.now().year + 5:
                self.add_error('graduation_year', "Graduation year seems too far in the future")
        
        # Validate company founding year
        if user and user.user_type == 'company':
            founded_year = cleaned_data.get('founded_year')
            if founded_year and founded_year > timezone.now().year:
                self.add_error('founded_year', "Founding year cannot be in the future")
        
        return cleaned_data