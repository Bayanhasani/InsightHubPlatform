from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
def welcome(request):
    return render(request,"pages/welcome.html")

@login_required(login_url='login')
def index(request):
    return render(request,"pages/index.html")
