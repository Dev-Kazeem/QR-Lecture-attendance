from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


app_name = 'Users_app'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.Login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('changePassword/', auth_views.PasswordChangeView.as_view(template_name='users/change_password.html', success_url="/Users_app/Password-changed"), name='changePassword'),
    
    path('Password-changed', views.Password_Changed, name='Password-changed' ),

]