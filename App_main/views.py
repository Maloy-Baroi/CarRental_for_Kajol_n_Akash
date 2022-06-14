from datetime import datetime, date
from datetime import datetime, date
from decimal import Decimal
from json import dumps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# from sslcommerz_python.payment import SSLCSession
from decimal import Decimal

from App_admin.views import is_admin
from App_authentication.forms import ProfileForm
from App_authentication.models import Profile
from App_main.models import Vehicles, CarBooking, BookingMoneyModel

# Create your views here.
# --------- Car Available Function -----------#
today = datetime.today().date()


def carAvailable(x):
    if len(x) == 0:
        return 0
    else:
        if today == x[0].pickup_date:
            x[0].car.is_available = False
            x[0].car.save()
        x.remove(x[0])
        return carAvailable(x)


def carDictionary(allCars, dataDictionary):
    if len(allCars) == 0:
        return dataDictionary
    else:
        dataDictionary[allCars[0].car_name] = [allCars[0].id, allCars[0].car_name, allCars[0].car_brand.name,
                                               allCars[0].car_number, allCars[0].color,
                                               f"{allCars[0].area.city}-{allCars[0].area.pincode}", allCars[0].capacity,
                                               allCars[0].doors, allCars[0].cost_per_day, allCars[0].is_available,
                                               allCars[0].description, allCars[0].car_image.url]
        allCars.remove(allCars[0])
        return carDictionary(allCars, dataDictionary)


# --------- Car Available Function End -----------#


def index(request):
    cars = Vehicles.objects.all()
    available_cars = cars.filter(is_available=True)[:6]
    carTypes = [x.car_brand for x in cars]
    carBookings = CarBooking.objects.all()
    carAvailable(list(carBookings))
    dataDictionary = carDictionary(list(cars), dict())
    dataJSON = dumps(dataDictionary)

    try:
        userAdmin = is_admin(request.user)
    except:
        userAdmin = False

    content = {
        'data': dataJSON,
        'carTypes': set(carTypes),
        'cars': available_cars,
        'userAdmin': userAdmin,
    }
    return render(request, 'App_main/home.html', context=content)


@login_required
def car_book(request, pk):
    car = Vehicles.objects.get(id=pk)
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.is_fully_filled():
            profile_done = True
        else:
            profile_done = False
    except:
        profile_done = False

    dictionary = {
        car.id: [car.id, car.car_name, car.car_brand.name, car.car_number, car.color, car.capacity, car.doors,
                 car.cost_per_day]}
    car_dictionary = dumps(dictionary)
    content = {
        'car': car,
        'profile_done': profile_done,
        'carDictionary': car_dictionary,
    }
    return render(request, 'App_main/car_booking.html', context=content)


@login_required
def confirm_booking(request):
    if request.method == 'POST':
        carID = request.POST.get('carID')
        theCar = Vehicles.objects.get(id=carID)
        pickupLocation = request.POST.get('pickupLocation')
        pickupCity = request.POST.get('pickupCity')
        pickupZipcode = request.POST.get('pickupZipcode')
        Phone = request.POST.get('Phone')
        pickupDate = request.POST.get('pickupDate')
        driverNeed = request.POST.get('driver-need')
        returnDate = request.POST.get('returnDate')
        rentPurpose = request.POST.get('rentPurpose')
        d0 = date(int(pickupDate[0:4]), int(pickupDate[5:7]), int(pickupDate[8:]))
        d1 = date(int(returnDate[0:4]), int(returnDate[5:7]), int(returnDate[8:]))
        if driverNeed:
            cost = int((d1 - d0).days * int(theCar.cost_per_day) + theCar.cost_per_day) + int(
                ((d1 - d0).days + 1) * 800)
        else:
            cost = int((d1 - d0).days * int(theCar.cost_per_day) + theCar.cost_per_day)
        paid = int(cost * 0.05)
        due = cost - paid

        booking = CarBooking(user=request.user, car_id=carID, contact_number=Phone, pickup_location=pickupLocation,
                             city=pickupCity, zipcode=pickupZipcode, pickup_date=pickupDate, need_driver=driverNeed,
                             return_date=returnDate, purpose_of_renting=rentPurpose, total_cost=cost, paid=paid,
                             due=due)
        booking.save()
        bookingMoney = BookingMoneyModel(booking=booking)
        bookingMoney.save()
        theCar.is_available = False
        theCar.save()
        return HttpResponseRedirect(reverse('App_main:payment', kwargs={"bookingID": int(booking.id)}))


@login_required
def view_profile(request):
    try:
        userProfile = Profile.objects.get(user=request.user)
        bookings = CarBooking.objects.filter(user=request.user)
    except:
        userProfile = None
        bookings = None
    form = ProfileForm(instance=userProfile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=userProfile)
        if form.is_valid():
            p = form.save(commit=False)
            p.user = request.user
            p.save()
            return HttpResponseRedirect(reverse('App_main:profile'))
    content = {
        'form': form,
        'userProfile': userProfile,
        'bookings': bookings,
    }
    return render(request, 'App_authentication/profile.html', context=content)


def car_showcasing(request):
    cars = Vehicles.objects.filter(is_available=True)
    content = {
        'cars': cars,
    }
    return render(request, 'App_main/car_showcasing.html', context=content)


@login_required
def cancel_booking(request, bookingID):
    booking = CarBooking.objects.get(id=bookingID)
    car_id = booking.car.id
    car = Vehicles.objects.get(id=car_id)
    car.is_available = True
    car.save()
    booking.delete()
    return HttpResponseRedirect(reverse('App_main:home'))


""" Payment System starts """


@login_required
def payment(request, bookingID):
    return redirect('App_main:home')
# @login_required
# def payment(request, bookingID):
#     current_user = request.user
#     profile = Profile.objects.get(user=request.user)
#     saved_address = f"{profile.House}, {profile.city}-{profile.zipcode}"
#     if not profile.is_fully_filled():
#         messages.info(request, "Please complete your profile details.")
#         return redirect('App_login:profile')
#
#     status_url = request.build_absolute_uri(reverse('App_main:purchased-complete'))
#     mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id="akcar62391d38d6184",
#                             sslc_store_pass="akcar62391d38d6184@ssl")
#     mypayment.set_urls(success_url=status_url, fail_url=status_url,
#                        cancel_url=status_url, ipn_url=status_url)
#
#     booking = CarBooking.objects.get(id=bookingID)
#     order_total = booking.total_cost - booking.due
#     order_item = booking.car.car_name
#     mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT',
#                                       product_category='car',
#                                       product_name=order_item, num_of_item=1, shipping_method='Courier',
#                                       product_profile='None')
#
#     mypayment.set_customer_info(name=profile.full_name, email=current_user.email,
#                                 address1=booking.pickup_location,
#                                 address2=saved_address, city=profile.city,
#                                 postcode=profile.zipcode, country="Bangladesh",
#                                 phone=booking.contact_number)
#
#     mypayment.set_shipping_info(shipping_to=profile.full_name, address=booking.pickup_location,
#                                 city=booking.city, postcode=booking.zipcode, country='Bangladesh')
#     response_data = mypayment.init_payment()
#
#     return redirect(response_data['GatewayPageURL'])
    # return HttpResponseRedirect(reverse('App_main:home'))


@csrf_exempt
def purchased_complete(request):
    if request.method == 'POST':
        payment_data = request.POST
        status = payment_data['status']
        amount = payment_data['amount']
        tran_date = payment_data['tran_date']
        currency = payment_data['currency']
        if status == 'VALID':
            bank_tran_id = payment_data['bank_tran_id']
            tran_id = payment_data['tran_id']
            val_id = payment_data['val_id']
            card_type = payment_data['card_type']
            return HttpResponseRedirect(
                reverse('App_main:complete-payment', kwargs={'val_id': val_id, 'tran_id': tran_id, }))
        elif status == 'FAILED':
            messages.warning(request, f"Your payment is failed")
        elif status == 'CANCELLED':
            messages.warning(request, "Your payment has been stopped!!!")

    if request.user.is_authenticated:
        cart_item = 1
    else:
        cart_item = 0
    content = {
        'cart_item': cart_item,
    }
    return render(request, 'App_main/complete_payment.html', context=content)


@login_required
def complete_payment(request, val_id, tran_id):
    this_booking = CarBooking.objects.get(user=request.user, booking_complete=False)
    booking_money = BookingMoneyModel.objects.get(booking=this_booking)
    booking_money.paymentID = val_id
    booking_money.amount = this_booking.paid
    booking_money.save()
    this_booking.booking_complete = True
    this_booking.save()
    return redirect('App_main:home')
