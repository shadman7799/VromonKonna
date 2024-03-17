from random import randint
from datetime import date

from django.http import HttpResponse
from django.shortcuts import redirect, render

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from .models import *
from blogs.models import *
from pkg.models import *

from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.core.mail import send_mail


def generate_username(email):
    email = email.lower().split("@")
    return email[0] + "_" + ".".join(email[1].split(".")[0:-1])


def generate_otp():
    otps = [x['first_name'] for x in User.objects.values(
        'first_name')]  # first_name field contains otp
    print(otps)
    otp = str(randint(100000, 999999))
    otp_hash = str(hash(otp))
    while otp_hash in otps:
        otp = str(randint(100000, 999999))
        otp_hash = str(hash(otp))
    return otp, otp_hash


def home(request):
    context = {
        'pkgs': Package.objects.all().order_by('-rating')[:5],
        'blogs': Blog.objects.all().order_by('-likes', '-comments')[:5],
    }
    return render(request, 'users/index.html', context)

def about_us(request):
    return render(request, 'users/about_us.html')


def join_us(request):
    return render(request, 'users/join_us.html')


def login_user(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            user = User.objects.get(email=email)
            username = generate_username(email)
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user:
                if 'on' in user.last_name.casefold():
                    subject = 'Two-step verification'
                    msg = 'Hi There.\nTo verify your account,'
                    send_mail_to_user(user, subject, msg)
                    return render(request, 'users/two_factor.html')

                login(request, user)
                return redirect('profile')

            user = User.objects.get(email=email)
            if not user.is_active:
                subject = 'Activate your account'
                msg = 'Hi There.\nTo activate account,'
                send_mail_to_user(user, subject, msg)
                return render(request, 'users/confirmation_page.html')
            else:
                messages.error(request, 'Wrong password')
            return render(request, 'users/login.html', {'email': email})
        except:
            messages.error(request, 'Invalid email')
            return render(request, 'users/login.html')

    return render(request, 'users/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def valid_hotel_info(request, context):
    if context['pass1'] != context['pass2']:
        messages.error(request, "Passwords don't match")
        return False

    if not context['hotline'].isnumeric():
        messages.error(request, "Hotline number must be numeric")
        return False
    hotlines = [x['hotline'] for x in HotelRep.objects.values('hotline')]
    if context['hotline'] in hotlines:
        messages.error(request, "This hotline number is already registered.")
        return False

    email = context['email']
    if User.objects.filter(email=email):
        messages.error(request, "Email is already used")
        return False

    if not is_valid_pass(context['pass1']):
        msg = 'Your password is weak!.\
                    \nPassword should have at least 8 characters.\
                    \nPassword should be a combination of \
                    upper and lowercase letters and digits.'
        messages.error(request, msg)
        return False

    return True


def hotel_reg(request):
    if request.method == 'POST':
        context = {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'address': request.POST['address'],
            'hotline': request.POST['hotline'],
            'catagory': request.POST['catagory'],
            'pass1': request.POST['pass1'],
            'pass2': request.POST['pass2'],
        }

        if not valid_hotel_info(request, context):
            return render(request, 'users/hotel_reg.html', context)

        user = User.objects.create_user(
            username=generate_username(context['email']),
            email=context['email'],
            password=context['pass1'],
            last_name='OFF_H',
            is_active=False
        )
        user.save()

        hotel_rep = HotelRep(user=user)
        hotel_rep.name = context['name']
        hotel_rep.address = context['address']
        hotel_rep.hotline = context['hotline']
        hotel_rep.catagory = context['catagory']
        hotel_rep.save()

        subject = 'Welcome to Vrmonkonna'
        msg = 'Hi There.\
                    \nThank you for registering in.\
                    \nTo activate account,'
        send_mail_to_user(user, subject, msg)

        return render(request, 'users/confirmation_page.html')

    return render(request, 'users/hotel_reg.html')


def valid_traveler_info(request, context):
    if request.POST['pass1'] != request.POST['pass2']:
        messages.error(request, "Passwords don't match")
        return False

    email = request.POST['email']
    if User.objects.filter(email=email):
        user = User.objects.get(email=email)
        if user.is_active:
            messages.error(request, "Email is already used")
            return False
        else:
            messages.error(request, "You're already registered.")
            return render(request, 'users/confirmation_page.html')

    if not (context['phone'].isnumeric() and context['e_phone'].isnumeric()) and len(context['phone']) == 11 and len(
            context['e_phone']) == 11:
        messages.error(
            request, "Phone number must be numeric & have 11 digits")
        return False

    phones = [x['phone'] for x in Traveler.objects.values('phone')]
    if context['phone'] in phones:
        messages.error(request, "This number is already registered.")
        return False

    if not context['nid'].isnumeric() or len(context['nid']) < 10:
        messages.error(request, "NID must be numeric & have 10 digits")
        return False

    nids = [x['national_id'] for x in Traveler.objects.values('national_id')]
    if context['nid'] in nids:
        messages.error(request, "This NID number is already registered.")
        return False

    if not (context['age'].isnumeric() and int(context['age']) >= 18):
        messages.error(request, "You must be at least 18 to join us.")
        return False

    if not is_valid_pass(context['pass1']):
        msg = 'Your password is weak!.\
                    \nPassword should have at least 8 characters.\
                    \nPassword should be a combination of \
                    upper and lowercase letters and digits.'
        messages.error(request, msg)
        return False

    return True


def traveler_reg(request):
    if request.method == 'POST':
        context = {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'address': request.POST['address'],
            'phone': request.POST['phone'],
            'e_phone': request.POST['e_phone'],
            'nid': request.POST['nid'],
            'bg': request.POST['bg'],
            'age': request.POST['age'],
            'pass1': request.POST['pass1'],
            'pass2': request.POST['pass2'],
        }

        if not valid_traveler_info(request, context):
            return render(request, 'users/traveler_reg.html', context)

        user = User.objects.create_user(
            username=generate_username(context['email']),
            email=context['email'],
            password=context['pass1'],
            last_name='OFF_T',
            is_active=False
        )
        user.save()

        traveler = Traveler(user=user)
        traveler.name = context['name']
        traveler.address = context['address']
        traveler.phone = context['phone']
        traveler.emergency_phone = context['e_phone']
        traveler.national_id = context['nid']
        traveler.blood_type = context['bg']
        traveler.age = context['age']
        traveler.save()

        subject = 'Welcome to Vrmonkonna'
        msg = 'Hi There.\
                    \nThank you for registering in.\
                    \nTo activate account,'
        send_mail_to_user(user, subject, msg)

        return render(request, 'users/confirmation_page.html')

    return render(request, 'users/traveler_reg.html')


def send_mail_to_user(user, subject, msg):
    otp, otp_hash = generate_otp()
    user.first_name = otp_hash
    user.save(update_fields=['first_name'])

    email_from = settings.EMAIL_HOST_USER
    email_to = [user.email]
    send_mail(
        subject,
        msg + f'\n\nEnter OTP: {otp}',
        email_from,
        email_to,
        fail_silently=True,
    )


def verify_acc(request):
    if request.method == 'POST':
        try:
            otp = str(hash(request.POST['otp']))
            user = User.objects.get(first_name=otp)
            user.is_active = True
            user.save()
            login(request, user)

            return redirect('profile')
        except:
            messages.error(request, 'Wrong OTP')

    return render(request, 'users/confirmation_page.html')


def two_factor(request):
    if request.method == 'POST':
        try:
            otp = str(hash(request.POST['otp']))
            user = User.objects.get(first_name=otp)
            login(request, user)
            return redirect('profile')
        except:
            messages.error(request, 'Wrong OTP')

    return render(request, 'users/two_factor.html')


@login_required(login_url='/login/')
def profile(request):
    try:
        return redirect('traveler_profile') if 'T' in request.user.last_name \
            else redirect('hotel_profile')
    except:
        return redirect('home')


@login_required(login_url='/login/')
def hotel_profile(request):
    context = {
        'data': request.user.hotelrep,
        'pkgs': Package.objects.filter(author=request.user.hotelrep).order_by('pk').reverse(),
        'blogs': Blog.objects.filter(author=request.user).order_by('pk').reverse(),
        'notifications': Notification.objects.filter(user=request.user, hidden=False).order_by('time').reverse(),
    }
    return render(request, 'users/hotel_profile.html', context)


@login_required(login_url='/login/')
def traveler_profile(request):
    bookings = list(Booking.objects.filter(traveler=request.user.traveler))
    curr_date = date.today()
    context = {
        'data': request.user.traveler,
        'blogs': Blog.objects.filter(author=request.user).order_by('pk').reverse(),
        'bookings': list(filter(lambda x: x.end_date >= curr_date, bookings)),
        'completed': list(filter(lambda x: x.end_date < curr_date, bookings)),
        'notifications': Notification.objects.filter(user=request.user, hidden=False).order_by('time').reverse(),
        'date': curr_date,
    }
    return render(request, 'users/traveler_profile.html', context)


def forget_pass(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'])
            subject = 'Reset your password'
            msg = 'Hi There.\nTo reset your password,'
            send_mail_to_user(user, subject, msg)
            return render(request, 'users/change_pass.html')
        except:
            messages.error(request, "Wrong email provided")

    return render(request, 'users/forget_pass.html')


def change_pass(request):
    if request.method == 'POST':
        try:
            otp = str(hash(request.POST['otp']))
            user = User.objects.get(first_name=otp)
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            if pass1 == pass2:
                if is_valid_pass(pass1):
                    user.set_password(pass1)
                    if not request.user.is_anonymous:
                        update_session_auth_hash(request, user)
                    user.save(update_fields=['password'])
                else:
                    msg = 'Your password is weak!.\
                                \n1. Password should have at least 8 characters.\
                                \n2. Password should be a combination of \
                                uppercase, lowercase letters and digits.'
                    messages.error(request, msg)
                    return render(request, 'users/change_pass.html', {'otp': otp})
            else:
                messages.error(request, "Password don't match")
                return render(request, 'users/change_pass.html', {'otp': otp})
        except:
            messages.error(request, "Wrong OTP")
            return render(request, 'users/change_pass.html')

    if request.user.is_authenticated:
        return redirect('profile')

    return render(request, 'users/login.html')


def is_valid_pass(password):
    # return True

    if len(password) < 8:
        return False

    error = 0
    if not any('a' <= ch <= 'z' for ch in password):
        error += 1
    if not any('A' <= ch <= 'Z' for ch in password):
        error += 1
    if not any(ch.isdigit() for ch in password):
        error += 1

    return True if not error else False


def manage_traveler_profile(request):
    info = request.user.traveler
    return render(request, 'users/manage_traveler_profile.html', {'data': info})


def save_traveler_info(request):
    traveler = request.user.traveler
    if request.method == 'POST':
        traveler.name = request.POST['name']
        traveler.phone = request.POST['phone']
        traveler.emergency_phone = request.POST['e_phone']
        traveler.address = request.POST['address']
        traveler.age = request.POST['age']
        traveler.blood_type = request.POST['blood_type']
        traveler.image = request.FILES['image'] if len(
            request.FILES) else traveler.image
        traveler.save()

        temp = request.user.last_name[-1]
        request.user.last_name = request.POST['two-factor'] + '_' + temp
        request.user.save()

        if 'save' in request.POST:
            return redirect('traveler_profile')
        elif 'change_pass' in request.POST:
            subject = 'Reset your password'
            msg = 'Hi There.\nTo reset your password,'
            send_mail_to_user(request.user, subject, msg)
            return render(request, 'users/change_pass.html')

    return render(request, 'users/manage_traveler_profile.html', {'data': traveler})


def manage_hotel_profile(request):
    info = request.user.hotelrep
    return render(request, 'users/manage_hotel_profile.html', {'data': info})


def save_hotel_info(request):
    hotel = request.user.hotelrep
    if request.method == 'POST':
        hotel.name = request.POST['name']
        hotel.hotline = request.POST['hotline']
        hotel.address = request.POST['address']
        hotel.image = request.FILES['image'] if len(
            request.FILES) else hotel.image
        hotel.save()

        temp = request.user.last_name[-1]
        request.user.last_name = request.POST['two-factor'] + '_' + temp
        request.user.save()

        if 'save' in request.POST:
            return redirect('hotel_profile')
        elif 'change_pass' in request.POST:
            subject = 'Reset your password'
            msg = 'Hi There.\nTo reset your password,'
            send_mail_to_user(request.user, subject, msg)
            return render(request, 'users/change_pass.html')

    return render(request, 'users/manage_hotel_profile.html', {'data': hotel})


def delete_msg(request, pk):
    msg = Notification.objects.filter(pk=pk).first()
    if msg:
        msg.hidden = True
        msg.save(update_fields=['hidden'])
    return redirect(request.META['HTTP_REFERER'])


def clear_all(request):
    Notification.objects.filter(
        user=request.user, hidden=False).update(hidden=True)
    return redirect(request.META['HTTP_REFERER'])


def notifications(request):
    msgs = Notification.objects.filter(user=request.user).order_by('time')
    return render(request, 'users/notifications.html', {'notifications': msgs})
