from django.shortcuts import render, get_object_or_404, redirect
from .models import CompanyProfile
from .forms import CompanyProfileForm  # type: ignore

# عرض جميع الشركات
def company_list(request):
    companies = CompanyProfile.objects.all()
    return render(request, 'templates/inf.html', {'companies': companies})
# إضافة شركة جديدة
def company_create(request):
    if request.method == "POST":
        form = CompanyProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inf')
    else:
        form = CompanyProfileForm()
    return render(request, 'templates/add.html', {'form': form})
# تعديل بيانات شركة
def company_update(request, pk):
    company = get_object_or_404(CompanyProfile, pk=pk)
    if request.method == "POST":
        form = CompanyProfileForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('inf')
    else:
        form = CompanyProfileForm(instance=company)
    return render(request, 'templates/add.html',{'form': form})
