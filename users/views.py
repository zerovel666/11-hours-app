from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from users.forms import *
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)
            if user:
                auth.login(request,user)
                messages.success(request,f"{username}, Вы вошли в аккаунт")
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Home - Авторизация',
        'form': form
    }
    return render(request,'users/login.html',context)
    
def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f"{User.username}, Вы успешно создали аккаунт")
            return HttpResponseRedirect(reverse('user:login'))
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'Home - Регистрация',
        'form' : form
    }
    return render(request,'users/registration.html',context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST,instance=request.user,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"{User.username}, Вы успешно обновили профиль аккаунт")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'title': 'Home - Регистрация',
        'form' : form
    }
    return render(request,'users/profile.html',context)

@login_required
def logout(request):
    messages.success(request,f"{request.user.username}, вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))

def users_cart(request):
    return render(request,'users/users_cart.html')