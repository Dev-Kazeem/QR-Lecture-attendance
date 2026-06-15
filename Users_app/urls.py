from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


app_name = 'Users_app'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.Login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]