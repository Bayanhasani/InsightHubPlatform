from django.urls import path
from . import views
app_name = 'website'  # 🔹 Define the app name

urlpatterns = [
    path('',views.welcome,name="welcome"),
    path('home',views.index,name="home"),
    
]
