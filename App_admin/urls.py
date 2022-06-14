from django.urls import path
from App_admin import views

app_name = 'App_admin'

urlpatterns = [
    path('admin-login-system/', views.admin_login_system, name='admin-login-system'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('all-users/', views.allUsers, name='all-users'),
    path('delete-user/<int:delete_id>/', views.delete_user, name='delete-user'),
    path('create-user/', views.create_user_by_admin, name='create-user'),
    path('all-profile-view/', views.allUserProfile, name='all-profile-view'),
    path('create-userProfile-by-admin', views.create_userProfile_by_admin, name='create-userProfile-by-admin'),
    path('see-area-by-admin', views.see_area_by_admin, name='see-area-by-admin'),
]


