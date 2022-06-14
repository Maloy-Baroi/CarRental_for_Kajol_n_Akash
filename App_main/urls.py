from django.urls import path
from App_main.views import *

app_name = 'App_main'

urlpatterns = [
    path('', index, name='home'),
    path('car-book/<int:pk>/', car_book, name='car-book'),
    path('profile/', view_profile, name='profile'),
    path('confirm-booking/', confirm_booking, name='confirm-booking'),
    path('car-showcasing/', car_showcasing, name='car-showcasing'),
    path('booking-cancel/<int:bookingID>/', cancel_booking, name='booking-cancel'),
    path('payment/<int:bookingID>/', payment, name='payment'),
    path('purchased-complete/', purchased_complete, name='purchased-complete'),
    path('complete-payment/<val_id>/<tran_id>/', complete_payment, name='complete-payment'),
]
