from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django import forms
from .models import Account
from django.contrib import messages, auth
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site 
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode



# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # build a username from the email local-part and ensure it's unique
            base_username = email.split('@')[0]
            username_candidate = base_username
            suffix = 1
            while Account.objects.filter(username=username_candidate).exists():
                username_candidate = f"{base_username}{suffix}"
                suffix += 1

            try:
                user = Account.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username_candidate,
                    email=email,
                    password=password,
                )
                user.phone_number = phone_number
                user.save()
            except IntegrityError:
                messages.error(request, 'A user with that email or username already exists. Please try a different email.')
                return redirect('accounts:register')
            #user activation
            # current_site = get_current_site(request)
            # mail_subject = 'Please activate your account'
            # message=render_to_string('accounts/account_verification_email.html',{
            #     'user':user,
            #     'domain':current_site,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':default_token_generator.make_token(user),
            #     'username': user.username,
            # })
            # to_email = email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)


            # messages.success(request, f'Registration successful. Your username is {user.username}. Check your email to activate your account.')
            # return redirect('accounts:login')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_view(request):
    if request.method == 'POST':        
        email = request.POST.get('name')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Login successful.')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html')

@login_required(login_url='accounts:login')
def logout_view(request):
   auth.logout(request)
   messages.info(request, 'You have been logged out.')
   return redirect('accounts:login')
def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully. You can now log in.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('accounts:register')
    
def dashboard(request):
    return render(request,'accounts/dashboard.html')
