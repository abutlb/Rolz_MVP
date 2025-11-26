from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # مسارات الأجهزة
    path('devices/', views.device_list, name='device_list'),
    path('devices/<int:pk>/', views.device_detail, name='device_detail'),
    path('devices/create/', views.create_device, name='create_device'),
    
    # مسارات التذاكر
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('tickets/<int:pk>/update-status/', views.update_ticket_status, name='update_ticket_status'),
]