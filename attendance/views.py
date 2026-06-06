from django.shortcuts import render, redirect



def Home_page(request):
    return render(request, 'attendance/home.html')
