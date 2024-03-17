import os
from datetime import date, timedelta
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from .models import *


def pkg_list(request):
    pkgs = list(Package.objects.all().order_by('-start_date'))
    if request.method == 'GET':
        try:
            text = request.GET['text'].lower()
            if text:
                pkgs = list(filter(lambda x: text in x.destination.casefold(
                ) or text in x.author.name.casefold(), pkgs))
            low = int(request.GET['min']) if request.GET['min'] else 0
            high = int(request.GET['max']) if request.GET['max'] else 999999
            if low or high:
                pkgs = list(filter(lambda x: low <= x.cost <= high, pkgs))
            context = {
                'pkgs': pkgs,
                'count': len(pkgs),
                'min': low if low != 0 else None,
                'max': high if high != 999999 else None,
                'text': text,
            }
            return render(request, 'pkg/packages.html', context)
        except:
            print('error search')
            pass
    count = len(pkgs)
    return render(request, 'pkg/packages.html', {'pkgs': pkgs, 'count': count})


def pkg_info(request, pk):
    pkg = Package.objects.get(pk=pk)
    curr_date = date.today()
    context = {
        'pkg': pkg,
        'reviews': Review.objects.filter(package=pkg).order_by('-pk'),
        'date': curr_date,
    }
    try:
        if pkg.author == request.user.hotelrep:
            context['author'] = True
    except:
        bookings = list(Booking.objects.filter(traveler=request.user.traveler))
        curr_bookings = list(filter(lambda x: x.package == pkg,bookings))
        if curr_bookings:
            context['booked'] = not all(booking.end_date < pkg.start_date for booking in curr_bookings)
        context['conflict'] = any(check_conflict(booking, pkg) for booking in bookings)
        context['bookable'] = curr_date < pkg.start_date
    return render(request, 'pkg/package_info.html', context)


def check_conflict(booking, pkg):
    return (booking.start_date <= pkg.start_date <= booking.end_date) or (booking.start_date <= pkg.end_date <= booking.end_date)


def traveler_list(request, pk):
    pkg = Package.objects.get(pk=pk)
    curr_date = date.today()
    bookings = list(Booking.objects.filter(package=pkg))
    bookings = list(
        filter(lambda x: x.package.start_date > curr_date, bookings))
    context = {
        'pkg': pkg,
        'bookings': bookings
    }
    return render(request, 'pkg/traveler_list.html', context)


def notify(request, pk):
    pkg = Package.objects.get(pk=pk)
    curr_date = date.today()
    bookings = list(Booking.objects.filter(package=pkg))
    bookings = list(
        filter(lambda x: x.package.start_date > curr_date, bookings))
    x = bookings[0]

    email_from = settings.EMAIL_HOST_USER
    email_to = [booking.email for booking in bookings]
    subject = "Upcoming tour with Vromonkonna"
    msg = f"Greetings from Vromonkonna.\
                        \nIt's our pleasure inform you that you've a tour planned with us.\
                        \n\nDestination: {x.package.destination} \
                        \nStart date: {x.package.start_date} \
                        \nOrganized by: {x.package.author.name} \
                        \nReporting time: 10:00 AM \
                        \n\nSee you soon."
    send_mail(subject, msg, email_from, email_to, fail_silently=True)
    messages.success(request, 'Notified travelers')

    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url="/login/")
def post_pkg(request):
    if request.method == 'POST':
        context = {
            'title': request.POST['title'],
            'dest': request.POST['dest'],
            'description': request.POST['text'],
            'cost': request.POST['cost'],
            'start': request.POST['start'],
            'end': request.POST['end'],
        }
        if len(request.FILES):
            image = PkgImage(user=request.user, image=request.FILES['image'])
            image.save()
            context['image'] = image

        if 'create' in request.POST:
            pkg = Package(author=request.user.hotelrep)
            set_pkg_values(pkg, context, request.user)
            return redirect('profile')

        return render(request, 'pkg/post_pkg.html', context)

    return render(request, 'pkg/post_pkg.html')


@login_required(login_url='/login/')
def edit_pkg(request, pk):
    pkg = Package.objects.get(pk=pk)

    context = {
        'title': pkg.title,
        'dest': pkg.destination,
        'description': pkg.description,
        'cost': pkg.cost,
        'start': pkg.start_date.strftime("%Y-%m-%d"),
        'end': pkg.end_date.strftime("%Y-%m-%d"),
        'image': pkg.image,
    }
    if request.method == 'POST' and pkg.author == request.user.hotelrep:
        curr_date = date.today()
        bookings = list(Booking.objects.filter(package=pkg))
        bookings = list(filter(lambda x: x.end_date > curr_date, bookings))
        if bookings:
            messages.error(request,
                           'Package is already booked by some users '
                           '\n You may change it after the tour takes place')
            return redirect(request.META['HTTP_REFERER'])

        context = {
            'title': request.POST['title'],
            'dest': request.POST['dest'],
            'description': request.POST['text'],
            'cost': request.POST['cost'],
            'start': request.POST['start'],
            'end': request.POST['end'],
            'image': pkg.image,
        }
        if len(request.FILES):
            image = PkgImage(user=request.user, image=request.FILES['image'])
            image.save()
            context['image'] = image.image

        if 'save' in request.POST:
            set_pkg_values(pkg, context, request.user)
            return redirect('profile')
        elif 'delete' in request.POST:
            # os.remove(pkg.image.path)
            pkg.delete()
            return redirect('profile')

        return render(request, 'pkg/edit_pkg.html', context)

    return render(request, 'pkg/edit_pkg.html', context)


def set_pkg_values(pkg, context, user):
    pkg.title = context['title']
    pkg.destination = context['dest']
    pkg.description = context['description']
    pkg.cost = context['cost']
    y, m, d = [int(x) for x in context['start'].split('-')]
    pkg.start_date = date(y, m, d)
    y, m, d = [int(x) for x in context['end'].split('-')]
    pkg.end_date = date(y, m, d)

    try:
        pkg.image = PkgImage.objects.get(user=user).image
    except:
        pass
    pkg.save()
    try:
        PkgImage.objects.filter(user=user).delete()
    except:
        pass


@login_required(login_url='/login/')
def book_pkg(request, pk):
    pkg = Package.objects.get(pk=pk)
    booking = Booking(
        package=pkg,
        traveler=request.user.traveler,
        start_date=pkg.start_date,
        end_date=pkg.end_date,
        email=request.user.email,
    )
    booking.save()
    msg = 'made a booking on your package.'
    create_notification(pkg, msg, request.user)
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login/')
def cancel_pkg(request, pk):
    pkg = Package.objects.get(pk=pk)
    bookings = Booking.objects.filter(
        package=pkg, traveler=request.user.traveler)
    temp = None
    for x in bookings:
        if x.end_date == pkg.end_date:
            temp = x
            break
    if temp:
        temp.delete()
    # return redirect('profile')
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login/')
def review(request, pk):
    try:
        review = Review.objects.get(package=Package.objects.get(
            pk=pk), traveler=request.user.traveler)
        if review:
            return redirect('edit_review', pk)
    except:
        return redirect('post_review', pk)


def post_review(request, pk):
    pkg = Package.objects.get(pk=pk)
    if request.method == 'POST':
        review = Review(package=pkg, traveler=request.user.traveler)
        set_review_values(request, review)
        update_pkg_review(pkg)
        msg = 'left a review on your package.'
        create_notification(pkg, msg, request.user)
        return redirect('profile')
    return render(request, 'pkg/post_review.html', {'pkg': pkg})


def edit_review(request, pk):
    if request.method == 'POST':
        pkg = Package.objects.get(pk=pk)
        review = Review.objects.get(
            package=pkg, traveler=request.user.traveler)
        if 'save' in request.POST:
            set_review_values(request, review)
        else:
            review.delete()
        update_pkg_review(pkg)

        return redirect('profile')

    context = {
        'pkg': Package.objects.get(pk=pk),
        'review': Review.objects.get(package=Package.objects.get(pk=pk), traveler=request.user.traveler)
    }
    return render(request, 'pkg/edit_review.html', context)


def set_review_values(request, review):
    review.rating = int(request.POST['rating'].split(' ')[0])
    review.description = request.POST['text']
    review.save()

    return


def update_pkg_review(pkg):
    reviews = Review.objects.filter(package=pkg).values('rating')
    stars = [x['rating'] for x in reviews]

    if stars:
        pkg.rating = sum(stars) / len(stars)
    pkg.total = len(stars)
    pkg.save()


def create_notification(pkg, msg, user):
    hotel = User.objects.get(hotelrep=pkg.author)
    notification = Notification(user=hotel, is_pkg=True)
    notification.message = f'{user.traveler.name} {msg}'
    notification.key = pkg.pk
    notification.save()
