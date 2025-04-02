from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from account.forms import CompanyVerificationForm
from company.form import CompanyProfileForm
def company_profile(request):
    company = get_object_or_404(company, id=1)
    return render(request, 'inf.html', {'company': company})

def company_create(request):
    if request.method == "POST":
        form = CompanyVerificationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('company_profile')
    else:
        form = CompanyProfileForm()
    
    return render(request, 'add.html', {'form': form, 'action': 'Create'})

def company_update(request, company_id):
    company = get_object_or_404(company, id=company_id)
    if request.method == "POST":
        form = CompanyProfileForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_profile')
    else:
        form =  CompanyProfileForm(instance=company)
    
    return render(request, 'add.html', {'form': form, 'action':'Update'})
