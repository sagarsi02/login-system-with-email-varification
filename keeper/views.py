from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def signUp(request):
    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        active = 0

        if password == c_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already in Use')
                return redirect('/login')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already is taken')
                return redirect('/')
            else:
                usr = User.objects.create_user(first_name=f_name, last_name=l_name, username=username, email=email, password=password, is_active=active)
                usr.save();
                messages.success(request, 'Successfully Account Created')
                return redirect('/login')

        else:
            messages.warning(request, 'Password not match')
            return redirect('/')
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            log_user = auth.authenticate(username=username, password=password)
            if log_user is not None:
                auth.login(request, log_user)
                return redirect('/home')
            else:
                messages.info(request, 'Password is Wrong')
                return render(request, 'login.html')
        else:
            messages.info(request, 'Username is not Exist')
            return render(request, 'login.html')
    else:        
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')