from django.shortcuts import render,redirect
from .forms import SignupForm,StudentVerificationForm,GraduateVerificationForm,CompanyVerificationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import CustomUser 
from .forms import GraduateVerificationForm

# sign up view
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save user but don’t commit yet
            user.is_verified = False  # Default to unverified
            user.save()
            request.session['pending_user_id'] = user.id  #  Store user ID in session for verification
            return redirect('verify_account')  # Redirect to verification page
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})



# verification view
def verify_account(request):
    user_id = request.session.get('pending_user_id')  #  Get user ID from session
    if not user_id:
        messages.error(request, "Session expired or no pending verification.")
        return redirect('signup')  #  Redirect if no user is found

    user = CustomUser.objects.get(id=user_id)  #  Get user from DB
    form = None

    # Select the correct form based on user type
    if user.user_type == 'graduate':
        form = GraduateVerificationForm(request.POST or None, request.FILES or None)
    elif user.user_type == 'student':
        form = StudentVerificationForm(request.POST or None)
    elif user.user_type == 'company':
        form = CompanyVerificationForm(request.POST or None)

    # When user submits the form (POST request)
    if form and request.method == 'POST' and form.is_valid():
        verification = form.save(commit=False)  # Don't save to DB yet
        verification.user = user  # Assign the logged-in user
        verification.verification_type = user.user_type  # Save user type
        verification.save()  # Save to the database

        messages.success(request, "Verification request submitted. Please wait for admin approval.")
        del request.session['pending_user_id']  # ✅ Remove session key after submission
        return redirect('login')  # ✅ Redirect to login page (user must wait for admin approval)
        
    return render(request, 'registration/verify.html', {'form': form})



# log in view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  # Authenticate user
        if user is not None:
            if user.is_verified:  #  Only allow verified users to log in
                login(request, user)
                return redirect('website:home')
            else:
                messages.error(request, "Your account is not verified yet. Please wait for admin approval.")
                return redirect('login')  
    return render(request, 'registration/login.html')   


# logout view
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

