from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import uuid

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
                token = uuid.uuid4()
                print(token)
                context ={
                    "title":"Technical First",
                    "Subject": "Varify Your Email Address",
                    "Desc": "Verify you Account by clicking on the button below Verify Button.",
                    "link": "http://127.0.0.1:8000/varifying/?token={0}".format(token),
                    "logo": "https://yt3.ggpht.com/ytc/AMLnZu-M5aWKmXmGhv23j3lKkB2YzjUspTKLGT4WXNFH=s900-c-k-c0x00ffffff-no-rj"
                }
                html_content = render_to_string("email.html", context)
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(
                    'Account Activation Link',
                    text_content,
                    'sagarsingh@grampower.com',
                    [usr.email]
                )
                email.attach_alternative(html_content, 'text/html')
                email.send()
                messages.success(request, 'Successfully Account Created... \n Please check your mail for account varification')
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
        if User.objects.filter(is_active = 1):
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
            messages.info(request, 'Please Varify your email... Check Your Email')
            return render(request, 'login.html')
    else:        
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')