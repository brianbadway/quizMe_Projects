from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import * 
import bcrypt

def index(request):
    return render(request, 'registration/login.html')

def to_create(request):
    return render(request,'registration/register.html')

def register(request):
    errors = User.objects.register_validator(request.POST)

    if len (errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/to_create')
    else: 
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
    request.session['user_id'] = user.id
    return redirect('/dashboard')

def login_render(request):
    return render(request, 'registration/login.html')

def login(request):  
    errors = User.objects.login_validator(request.POST)
    if len (errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.filter(email=request.POST['email'])

    request.session['user_id'] = user[0].id
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/login_page')