from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django_countries.fields import CountryField
from django.core.validators import *
from django.contrib.auth.models import User, PermissionsMixin
from django.utils.translation import gettext_lazy as _


# Create your models here.
class MyUserManager(BaseUserManager):
    """ A custom Manager to deal with emails as unique identifer """

    def _create_user(self, email, password, **extra_fields):
        """ Creates and saves a user with a given email and password"""

        if not email:
            raise ValueError("The Email must be set!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log in this site')
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts')
    )

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


phone_regex = RegexValidator(regex=r"^\+?(88)01[3-9][0-9]{8}$", message=_('Enter Bangladeshi Number with country code'))


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=264, blank=True, null=True)
    full_name = models.CharField(max_length=264, blank=True, null=True)
    phone_number = models.CharField(validators=[phone_regex], verbose_name=_("Mobile phone"), max_length=17,
                                    blank=True, null=True)
    country = CountryField(blank_label='(select country)', null=True)
    House = models.TextField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='profile_picture/')
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username + "'s Profile"

    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]
        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True


class ContactUsModel(models.Model):
    Name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
