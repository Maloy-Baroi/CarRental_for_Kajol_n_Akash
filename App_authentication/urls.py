from django.urls import path
from App_authentication.views import signup_system, login_system, logout_system

app_name = 'App_authentications'

urlpatterns = [
    path('signup/', signup_system, name='signup'),
    path('login/', login_system, name='login'),
    path('logout/', logout_system, name='logout'),
]
