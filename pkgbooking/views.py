import os
from datetime import datetime

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import *


def pkg_list(request):
    pass


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
            pkg = Package(hotel=request.user.hotelrep)
            set_pkg_values(pkg, context, request.user)
            return redirect('profile')

        return render(request, 'pkg/post_pkg.html', context)

    return render(request, 'pkg/post_pkg.html')


def edit_pkg(request):
    pass


def set_pkg_values(pkg, context, user):
    pkg.title = context['title']
    pkg.destination = context['dest']
    pkg.description = context['description']
    pkg.cost = context['cost']
    date = context['start'].split('/')
    pkg.start = context['start']
    pkg.end = context['end']
    try:
        pkg.image = PreviewImage.objects.get(user=user).image
    except:
        pass
    pkg.save()
    try:
        PreviewImage.objects.get(user=user).delete()
    except:
        pass
