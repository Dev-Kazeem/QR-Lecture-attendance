from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django import forms






def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='Users_app.backends.EmailOrUsernameBackend')  # Auto-login after signup
            messages.success(request, "Your account is created successful!")
            if user.is_staff:
                return redirect('attendance_app:lecturer_dashboard') # you’ll create this
            else:
                print(form.errors)
                return redirect('attendance_app:scan_page') # student scan page
        messages.error(request, "Invalid credentials check and try again")  
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})




def Login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, "You're logged successful!")
            if user.is_staff:
                return redirect('attendance_app:lecturer_dashboard') # Redirect lecturer to their dashboard after login
            else: 
                return redirect('attendance_app:scan_page') # Redirect student to scan page after login
        messages.error(request, "Invalid username or password check and try again")
    return render(request, 'users/login.html') 


def LogoutView(request):
    if request.method == 'POST':
        logout(request)
        return redirect('Users_app:login')




class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Current Password')
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

@login_required
def Password_Changed(request):
    messages.success(request, 'Password changed successfully')
    return render(request, 'users/password_changed.html')
