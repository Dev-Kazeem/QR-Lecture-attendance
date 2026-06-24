from django import forms
from django.contrib.auth.forms import UserCreationForm
from Users_app.models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    student_id = forms.CharField(max_length=20, required=True)
   

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'student_id', 'password1', 'password2']
    
    def clean_student_id(self):
        sid = self.cleaned_data['student_id'].strip().upper()

        if not sid:
            raise forms.ValidationError("student ID is required for student signup")

        if User.objects.filter(student_id=sid).exists():
             raise forms.ValidationError("student ID already exists")
        return sid
    

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
             raise forms.ValidationError("Email already exists")
        return email
    

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username=username).exists():
             raise forms.ValidationError("Username already exists")
        return username