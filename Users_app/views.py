from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm



def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup
            if user.is_staff:
                return redirect('attendance_app:lecturer_dashboard') # you’ll create this
            else:
                return redirect('attendance_app:scan_page') # student scan page
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})


def LogoutView(request):
    if request.method == 'POST':
        logout(request)
        return redirect('Users_app:login')

