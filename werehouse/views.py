from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # возможност приминения форм из шаблона
from django.contrib.auth.models import User # импортирую модель
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
#
def home(request):
    return render(request, 'werehouse/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'werehouse/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # создать нового пользователя
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('filebox') # переходим на эту страницу
            except IntegrityError:
                return render(request, 'werehouse/signupuser.html', {'form': UserCreationForm(),
                                                                     'error': 'this username is taken,'
                                                                              'please choose another name'})
        else:
            return render(request, 'werehouse/signupuser.html', {'form': UserCreationForm(),
                                                                 'error': 'Password mismatch'})

def filebox(request):
    return render(request, 'werehouse/filebox.html')


def filepush(request):
    return render(request, 'werehouse/filepush.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'werehouse/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'werehouse/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and password didnt match'})
        else:
            login(request, user)
            return redirect('filebox')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
