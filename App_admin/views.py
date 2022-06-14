from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from App_authentication.models import *

# Create your views here.
from App_main.models import Area, CarBooking


@login_required
def admin_dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None
    content = {
        'profile': profile,
    }
    return render(request, 'App_admin/dashboard.html', context=content)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def password_rewriter(username):
    try:
        user = CustomUser.objects.get(email=username)
        if user.last_login is None:
            user.set_password(user.password)
            user.save()
    except:
        return False


def admin_login_system(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        user_email = request.POST.get('username')
        password = request.POST.get('password')
        form = AuthenticationForm(data=request.POST)
        password_rewrite = password_rewriter(user_email)
        if form.is_valid():
            user = authenticate(username=user_email, password=password)
            if user:
                login(request, user)
                if is_admin(user):
                    return HttpResponseRedirect(reverse('App_admin:admin-dashboard'))
                return HttpResponseRedirect(reverse('App_admin:admin-login-system'))
    content = {
        'form': form
    }
    return render(request, 'App_admin/login_page.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
def allUsers(request):
    users = CustomUser.objects.filter(is_superuser=False)

    content = {
        'users': users
    }
    return render(request, 'App_admin/all_users.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
def create_user_by_admin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = CustomUser(email=email)
    user.set_password(password)
    user.is_superuser = False
    user.is_active = True
    user.is_staff = False
    user.save()

    return HttpResponseRedirect(reverse('App_admin:all-users'))


@login_required(login_url='App_admin:admin-login-system')
def delete_user(request, delete_id):
    user = CustomUser.objects.get(id=delete_id)
    user.delete()
    return HttpResponseRedirect(reverse('App_admin:all-users'))


@login_required(login_url='App_admin:admin-login-system')
def allUserProfile(request):
    profiles = Profile.objects.filter(user__is_superuser=False)
    users = CustomUser.objects.filter(is_superuser=False)
    content = {
        'profiles': profiles,
        'users': users,
    }
    return render(request, 'App_admin/all_profile.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def create_userProfile_by_admin(request):
    userEmail = request.POST.get('user')
    userID = CustomUser.objects.get(email=userEmail)
    username = request.POST.get('username')
    Full_Name = request.POST.get('Full_Name')
    Mobile = request.POST.get('Mobile')
    House = request.POST.get('House')
    City = request.POST.get('City')
    ZipCode = request.POST.get('ZipCode')
    Profile_Picture = request.FILES['Profile_Picture']
    userProfile = Profile(username=username, full_name=Full_Name, phone_number=Mobile, country='Bangladesh',
                          House=House, city=City, zipcode=ZipCode, profile_picture=Profile_Picture)
    userProfile.user = userID
    userProfile.save()

    return HttpResponseRedirect(reverse('App_admin:all-profile-view'))


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def see_area_by_admin(request):
    areas = Area.objects.all()
    if request.method == 'POST':
        city = request.POST.get('City')
        Zipcode = request.POST.get('ZipCode')
        area = Area(city=city, pincode=Zipcode)
        area.save()
    content = {
        'areas': areas
    }
    return render(request, 'App_admin/areaModel.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def see_area_by_admin(request):
    carBookings = CarBooking.objects.all()
    content = {
        'carBookings': carBookings,
    }
    return render(request, 'App_admin/carBooking.html', context=content)
