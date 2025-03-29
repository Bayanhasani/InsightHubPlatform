from django import forms
from .models import post
class postForm(forms.ModelForm):
    class Mete:
        model=post
        fields =["content","image"]