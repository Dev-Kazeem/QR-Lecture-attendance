from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup
            messages.success(request, "Your account is created successful!")
            if user.is_staff:
                return redirect('attendance_app:lecturer_dashboard') # you’ll create this
            else:
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
            messages.success(request, "You're login successful!")
            if user.is_staff:
                return redirect('attendance_app:lecturer_dashboard') # Redirect lecturer to their dashboard after login

            return redirect('attendance_app:scan_page') # Redirect student to scan page after login
        messages.error(request, "Invalid username or password check and try again")
    return render(request, 'users/login.html') 


def LogoutView(request):
    if request.method == 'POST':
        logout(request)
        return redirect('Users_app:login')





"""
from django.contrib.auth.decorators import user_passes_test
import csv
import io
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .forms import CSVUploadForm

@user_passes_test(lambda u: u.is_superuser)  # only superuser can create accounts
def create_user(request):
    if request.method == 'POST':
        form =SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Users_app:user_list')
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})




@user_passes_test(lambda u: u.is_superuser) # superuser creating more then one user at once
def bulk_create_students(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            created_count = 0
            errors = []
            
            for row in reader:
                try:
                    username = row['username'].strip()
                    email = row['email'].strip()
                    first_name = row['first_name'].strip()
                    last_name = row['last_name'].strip()
                    student_id = row['student_id'].strip()
                    
                    # Skip if user exists
                    if User.objects.filter(username=username).exists():
                        errors.append(f"{username} already exists")
                        continue
                    
                    # Create user. Student = is_staff=False
                    password = User.objects.make_random_password(length=8)
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                        is_staff=False
                    )
                    
                    # Create profile with student_id
                    Profile.objects.create(user=user, student_id=student_id)
                    
                    # You can print/log passwords or export them to CSV for distribution
                    print(f"Created {username} - password: {password}")
                    created_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {reader.line_num}: {str(e)}")
            
            messages.success(request, f"Created {created_count} students successfully.")
            if errors:
                messages.warning(request, f"Errors: {'; '.join(errors[:5])}")
            
            return redirect('attendance:user_list')
    else:
        form = CSVUploadForm()
    
    return render(request, 'attendance/bulk_upload.html', {'form': form})


"""