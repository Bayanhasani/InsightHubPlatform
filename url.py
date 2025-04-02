from django.urls import path
from .views import company_list, company_create, company_update
urlpatterns = [
    path('companies/', company_list, name='company_list'),
    path('companies/new/', company_create, name='company_create'),
    path('companies/<int:pk>/edit/', company_update, name='company_update'),
]
#يسمح برفع صور الشعاراات وحغظها في مجلد اسمه media
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)