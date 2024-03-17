from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.pkg_list, name='pkg_list'),
    path('post_pkg/', views.post_pkg, name='post_pkg'),
    path('edit_pkg/<int:pk>', views.edit_pkg, name='edit_pkg'),
]
