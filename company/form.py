from django import forms
from .models import CompanyProfile
class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['name', 'description', 'email', 'phone', 'address', 'website','logo']
