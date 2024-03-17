from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.pkg_list, name='pkg_list'),
    path('post_pkg/', views.post_pkg, name='post_pkg'),
    path('edit_pkg/<int:pk>', views.edit_pkg, name='edit_pkg'),
    path('package/<int:pk>', views.pkg_info, name='pkg_info'),
    path('traveler_list/<int:pk>', views.traveler_list, name='traveler_list'),
    path('notify/<int:pk>', views.notify, name='notify'),
    path('book_package/<int:pk>', views.book_pkg, name='book_pkg'),
    path('cancel_package/<int:pk>', views.cancel_pkg, name='cancel_pkg'),
    path('review/<int:pk>', views.review, name='review'),
    path('post_review/<int:pk>', views.post_review, name='post_review'),
    path('edit_review/<int:pk>', views.edit_review, name='edit_review'),
]
