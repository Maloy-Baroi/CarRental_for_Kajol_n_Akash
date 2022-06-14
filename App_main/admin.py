from django.contrib import admin
from App_main.models import Vehicles, Area, CarDriver, CarBrand, CarBooking, BookingMoneyModel

# Register your models here.
admin.site.register(Area)
admin.site.register(Vehicles)
admin.site.register(CarDriver)
admin.site.register(CarBrand)
admin.site.register(CarBooking)
admin.site.register(BookingMoneyModel)
