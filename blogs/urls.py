from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('blog/<int:pk>', views.blog_post, name='blog_post'),
    path('post_blog/', views.post_blog, name='post_blog'),
    path('edit_blog/<int:pk>', views.edit_blog, name='edit_blog'),
    path('delete_comment/<int:pk>', views.delete_comment, name='delete_comment'),
]
