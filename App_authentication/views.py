import re
import uuid
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User, Group

# Create your views here.
from django.urls import reverse

from App_authentication.forms import SignUpForm, ProfileForm, ContactUsForm
from App_authentication.models import Profile, CustomUser


def signup_system(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.save()
            customer_group = Group.objects.get_or_create(name="CUSTOMER")
            customer_group[0].user_set.add(user)
            return HttpResponseRedirect(reverse('App_authentications:login'))
    content = {
        'form': form,
    }
    return render(request, 'App_authentication/signup_page.html', context=content)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def login_system(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=user_email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('App_main:home'))
    content = {
        'form': form
    }
    return render(request, 'App_authentication/login_page.html', context=content)


def logout_system(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_main:home'))

