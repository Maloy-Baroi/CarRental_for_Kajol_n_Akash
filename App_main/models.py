from django.db import models
from django.core.validators import *
from App_authentication.models import CustomUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Area(models.Model):
    pincode = models.CharField(validators=[MinLengthValidator(4), MaxLengthValidator(6)], max_length=6, unique=True)
    city = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.city}-{self.pincode}"


class CarDriver(models.Model):
    car_driver = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    NID = models.CharField(max_length=17, validators=[MinLengthValidator(10), MaxLengthValidator(17)], default=0)
    Driving_licence = models.CharField(max_length=20)
    Photo = models.ImageField(null=False, blank=False, upload_to='drivers/')
    mobile = models.CharField(validators=[MinLengthValidator(11), MaxLengthValidator(14)], max_length=14)
    area = models.OneToOneField(Area, on_delete=models.PROTECT)
    wallet = models.IntegerField(default=0)


class CarBrand(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.name


class Vehicles(models.Model):
    car_name = models.CharField(max_length=20)
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name='Brand')
    driver = models.ForeignKey(CarDriver, on_delete=models.PROTECT, null=True, blank=True)
    car_number = models.CharField(max_length=50)
    color = models.CharField(max_length=10)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    capacity = models.CharField(max_length=2)
    doors = models.IntegerField(null=False, default=0, blank=False)
    cost_per_day = models.IntegerField(null=False, blank=False, default=0)
    is_available = models.BooleanField(default=True)
    description = models.TextField()
    car_image = models.ImageField(upload_to='car-image/', blank=True)

    def __str__(self):
        return f"{self.car_name}"


phone_regex = RegexValidator(regex=r"^\+?(88)01[3-9][0-9]{8}$", message=_('Enter Bangladeshi Number with country code'))


class CarBooking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer')
    car = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='car')
    contact_number = models.CharField(validators=[phone_regex], verbose_name=_("Mobile phone"), max_length=17,
                                      blank=True, null=True)
    pickup_location = models.TextField()
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    pickup_date = models.DateField()
    need_driver = models.BooleanField()
    return_date = models.DateField()
    purpose_of_renting = models.TextField()
    total_cost = models.IntegerField()
    paid = models.IntegerField()
    due = models.IntegerField()
    booking_complete = models.BooleanField(default=False)


class BookingMoneyModel(models.Model):
    booking = models.ForeignKey(CarBooking, on_delete=models.CASCADE, related_name='booking')
    amount = models.IntegerField(default=0)
    paymentID = models.CharField(max_length=100, null=True)

