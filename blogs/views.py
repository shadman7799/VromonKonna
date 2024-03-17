import os

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from users.models import Notification

from .models import *


def blog_list(request):
    blogs = Blog.objects.all().order_by('pk').reverse()
    if request.method == 'GET':
        try:
            blogs = list(blogs)
            type = request.GET['filter']
            if type != 'See All':
                if type == 'Traveler':
                    blogs = list(
                        filter(lambda blog: 'T' in blog.author.last_name, blogs))
                else:
                    blogs = list(
                        filter(lambda blog: 'H' in blog.author.last_name, blogs))
            dest = request.GET['dest']
            if dest:
                blogs = list(filter(lambda blog: dest.lower() in blog.destination.casefold(
                ) or dest.lower() in blog.title.casefold(), blogs))
            print('done')
            context = {
                'filter': type,
                'dest': dest,
                'blogs': blogs,
                'count': len(blogs)
            }

            print('done')
            return render(request, 'blogs/blog_list.html', context)
        except:
            print('search error')
            pass

    count = len(blogs)
    return render(request, 'blogs/blog_list.html', {'blogs': blogs, 'count': count})


@login_required(login_url='/login/')
def blog_post(request, pk):
    blog = Blog.objects.get(pk=pk)
    if request.method == 'POST':
        if 'like' in request.POST:
            blog.likes += 1
            liked = BlogLike(author=request.user, blog=blog)
            liked.save()
            if blog.author != request.user:
                create_notification(blog, 'liked', request.user)
        elif 'unlike' in request.POST:
            blog.likes -= 1 if blog.likes > 0 else 0
            try:
                BlogLike.objects.filter(blog=blog, author=request.user).delete()
            except:
                return redirect(request.META['HTTP_REFERER'])
        else:
            if len(request.POST['text']):
                blog.comments += 1
                comment = BlogComment(
                    author=request.user, blog=blog, comment=request.POST['text'])
                comment.save()
                if blog.author != request.user:
                    create_notification(blog, 'commented on', request.user)
        blog.save()
        return redirect(request.META['HTTP_REFERER'])

    context = get_blog_content(blog)
    if BlogLike.objects.filter(blog=blog, author=request.user):
        context['liked'] = True
    return render(request, 'blogs/blog_post.html', context)


def create_notification(blog, arg, user):
    notification = Notification(user=blog.author, is_blog=True)
    if 'T' in user.last_name:
        notification.message = f'{user.traveler.name} {arg} your blog.'
    else:
        notification.message = f'{user.hotelrep.name} {arg} your blog.'
    notification.key = blog.pk
    notification.save()


def get_blog_content(blog):
    comments = BlogComment.objects.filter(blog=blog)
    author = blog.author.traveler if 'T' in blog.author.last_name else blog.author.hotelrep
    context = {
        'blog': blog,
        'total_comments': len(comments),
        'author': author,
        'comments': comments,
    }
    return context


@login_required(login_url='/login/')
def post_blog(request):
    if request.method == 'POST':
        context = {
            'title': request.POST['title'],
            'dest': request.POST['dest'],
            'thoughts': request.POST['text'],
        }
        if len(request.FILES):
            image = PreviewImage(
                user=request.user, image=request.FILES['image'])
            image.save()
            context['image'] = image

        if 'create' in request.POST:
            blog = Blog(author=request.user)
            set_blog_values(blog, context, request.user)
            return redirect('profile')

        return render(request, 'blogs/post_blog.html', context)

    return render(request, 'blogs/post_blog.html')


@login_required(login_url='/login/')
def edit_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    context = {
        'title': blog.title,
        'dest': blog.destination,
        'thoughts': blog.thoughts,
        'image': blog.image
    }
    if request.method == 'POST' and blog.author == request.user:
        context = {
            'title': request.POST['title'],
            'dest': request.POST['dest'],
            'thoughts': request.POST['text'],
        }
        if len(request.FILES):
            image = PreviewImage(
                user=request.user, image=request.FILES['image'])
            image.save()
            context['image'] = image.image

        if 'save' in request.POST:
            set_blog_values(blog, context, request.user)
            return redirect('profile')
        elif 'delete' in request.POST:
            # os.remove(blog.image.path)
            blog.delete()
            return redirect('profile')

        return render(request, 'blogs/edit_blog.html', context)

    return render(request, 'blogs/edit_blog.html', context)


def set_blog_values(blog, context, user):
    blog.title = context['title']
    blog.destination = context['dest']
    blog.thoughts = context['thoughts']
    try:
        blog.image = PreviewImage.objects.get(user=user).image
    except:
        pass
    blog.save()
    try:
        PreviewImage.objects.get(user=user).delete()
    except:
        pass


# return redirect(request.META['HTTP_REFERER'])
@login_required(login_url='/login/')
def delete_comment(request, pk):
    try:
        comment = BlogComment.objects.get(pk=pk)
        blog = Blog.objects.get(blogcomment=comment)
        blog.comments -= 1 if blog.comments > 0 else 0
        blog.save()
        comment.delete()
    except:
        pass
    return redirect(request.META['HTTP_REFERER'])
