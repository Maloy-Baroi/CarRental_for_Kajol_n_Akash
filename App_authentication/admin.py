from django.contrib import admin
from App_authentication.models import Profile, CustomUser, ContactUsModel


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(ContactUsModel)
