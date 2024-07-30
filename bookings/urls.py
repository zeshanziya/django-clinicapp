from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('manage/', views.manage_bookings, name='manage_bookings'),
    path('update-status/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
    path('<str:date>/', views.booking_slots, name='booking_slots'),
    path('confirmation/<str:date>/<str:time>/', views.booking_confirmation, name='booking_confirmation'),

]
