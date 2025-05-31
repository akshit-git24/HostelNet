from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('register/university/', views.register_university, name='register_university'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('apply/', views.apply_hostel, name='apply_hostel'),
    path('status/<int:application_id>/', views.application_status, name='application_status'),
    
    # University admin URLs
    path('university/dashboard/', views.university_dashboard, name='university_dashboard'),
    path('university/hostel/add/', views.manage_hostel, name='add_hostel'),
    path('university/hostel/<int:hostel_id>/edit/', views.manage_hostel, name='edit_hostel'),
    path('university/hostel/<int:hostel_id>/', views.view_hostel, name='view_hostel'),
    path('university/hostel/<int:hostel_id>/room/add/', views.manage_room, name='add_room'),
    path('university/hostel/<int:hostel_id>/room/<int:room_id>/edit/', views.manage_room, name='edit_room'),
    
    # AJAX URLs
    path('ajax/load-rooms/', views.load_rooms, name='ajax_load_rooms'),
] 