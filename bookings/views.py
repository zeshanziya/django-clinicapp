from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Booking
from django.utils.dateparse import parse_date

@login_required
def calendar_view(request):
    return render(request, 'bookings/calendar.html')

@login_required
def booking_slots(request, date):
    slots = [
        ("3:00 PM", "3:00 PM"),
        ("3:30 PM", "3:30 PM"),
        ("4:00 PM", "4:00 PM"),
        ("4:30 PM", "4:30 PM"),
        ("5:00 PM", "5:00 PM"),
        ("5:30 PM", "5:30 PM"),
        ("6:00 PM", "6:00 PM"),
        ("6:30 PM", "6:30 PM"),
        ("7:00 PM", "7:00 PM"),
        ("7:30 PM", "7:30 PM")
    ]

    date_obj = parse_date(date)
    booked_slots = Booking.objects.filter(date=date_obj).values_list('time', flat=True)

    if request.method == 'POST':
        selected_time = request.POST.get('slot')
        if selected_time not in booked_slots:
            Booking.objects.create(user=request.user, date=date, time=selected_time)
            return redirect('bookings:booking_confirmation', date=date, time=selected_time)

    context = {
        'date': date,
        'slots': slots,
        'booked_slots': booked_slots
    }
    return render(request, 'bookings/slots.html', context)

@login_required
def booking_confirmation(request, date, time):
    return render(request, 'bookings/confirmation.html', {'date': date, 'time': time})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('date', 'time')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        return redirect('bookings:my_bookings')
    return render(request, 'bookings/cancel_booking.html', {'booking': booking})

def staff_or_superuser(user):
    return user.is_staff or user.is_superuser

@user_passes_test(staff_or_superuser)
@login_required
def manage_bookings(request):
    bookings = Booking.objects.all().order_by('date', 'time')
    return render(request, 'bookings/manage_bookings.html', {'bookings': bookings})

@user_passes_test(staff_or_superuser)
@login_required
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.status = status
        booking.save()
        return redirect('bookings:manage_bookings')
    return render(request, 'bookings/update_booking_status.html', {'booking': booking, 'status': status})
