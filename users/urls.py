from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('join_us/', views.join_us, name='join_us'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('hotel_reg/', views.hotel_reg, name='hotel_reg'),
    path('traveler_reg/', views.traveler_reg, name='traveler_reg'),
    path('profile/', views.profile, name='profile'),
    path('hotel_profile/', views.hotel_profile, name='hotel_profile'),
    path('traveler_profile/', views.traveler_profile, name='traveler_profile'),
    path('confirmation_page/', views.verify_acc, name='confirmation_page'),
    path('forget_pass/', views.forget_pass, name='forget_pass'),
    path('change_pass/', views.change_pass, name='change_pass'),
    path('two_factor/', views.two_factor, name='two_factor'),
    path('manage_traveler_profile/', views.manage_traveler_profile, name='manage_traveler_profile'),
    path('save_traveler_info/', views.save_traveler_info, name='save_traveler_info'),
    path('manage_hotel_profile/', views.manage_hotel_profile, name='manage_hotel_profile'),
    path('save_hotel_info/', views.save_hotel_info, name='save_hotel_info'),
    path('delete_msg/<int:pk>', views.delete_msg, name='delete_msg'),
    path('notifications/', views.notifications, name='notifications'),
    path('clear_all/', views.clear_all, name='clear_all'),
    path('about_us/', views.about_us, name='about_us'),
]
