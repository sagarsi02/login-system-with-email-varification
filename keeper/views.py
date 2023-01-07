from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import usr_token
from django.core.mail import send_mail
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
                profilr_usr = usr_token.objects.create(user=usr.id, token=token)
                profilr_usr.save()
                print(token)
                context ={
                    "users": "Hii {0}, ".format(usr.first_name),
                    "title":"Technical First",
                    "Subject": "Varify Your Account",
                    "Desc": "Please Verify your Account by clicking on the below Verify Button.",
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
        if User.objects.filter(username=username).exists():
            account_activated = User.objects.filter(username=username).values('is_active')[0]['is_active']
            if account_activated == True:
                log_user = auth.authenticate(username=username, password=password)
                if log_user is not None:
                    auth.login(request, log_user)
                    return redirect('/home')
                else:
                    messages.info(request, 'Password is Wrong')
                    return render(request, 'login.html')
            else:
                messages.info(request, 'Please Varify your email... Check Your Email')
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

def varifying(request):
    get_token = request.GET.get('token')
    get_id = usr_token.objects.filter(token=get_token).values('user')[0]['user']
    already_varified = User.objects.filter(id=get_id).values('is_active')[0]['is_active']
    if already_varified == True:
        messages.info(request, 'Account already Verified please logged in.')
        return redirect('/login')
    else:
        cursor = connection.cursor()
        query = '''
            UPDATE 
                auth_user
            SET 
                is_active = 1 
            WHERE 
                id = {0};
        '''.format(get_id)
        cursor.execute(query)
        connection.commit()
        messages.info(request, 'Account Verified')
        return redirect('/login')


def password_forget(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        get_user_id = User.objects.get(username=username).id
        get_user_email = User.objects.get(username=username).email
        get_token = usr_token.objects.get(user=get_user_id).token
        send_mail(
            'Password Reset',
            'Click here to forget your Password : \nhttp://127.0.0.1:8000/password_reset/?token={0}.'.format(get_token),
            'sagarsingh@grampower.com',
            [get_user_email],
            fail_silently=False,
        )
        messages.info(request, 'Password Reset link send in your email. please check your email.')
        return redirect('/login')
    else:
        return render(request, 'forgetPassword.html')

def password_reset(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        get_token = request.GET.get('token')
        if password == c_password: 
            get_id = usr_token.objects.filter(token=get_token).values('user')[0]['user']
            query = '''
                
            '''
            return redirect('/password_reset')
        else:
            messages.info(request, 'Password do not match')
            return redirect('/password_reset/?token={0}'.format(get_token))
    else:
        return render(request, 'password_reset.html')