from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import StaffForm
from .models import Problem  # Import the Problem model
from bookings.models import Booking

def register(request):
    next_url = request.GET.get('next', 'home')
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            problem = form.cleaned_data['problem']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()

                # Create the Problem instance
                if problem:
                    Problem.objects.create(user=user, description=problem)

                login(request, user)
                return redirect(next_url)
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = StaffForm()

    return render(request, 'accounts/register.html', {'form': form, 'next': next_url})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def add_staff(request):
    form = None  # Initialize form variable

    if request.method == 'POST':
        action = request.POST.get('action')
        search_query = request.POST.get('search_query')

        if action == 'search':
            if search_query:
                try:
                    staff = User.objects.get(email=search_query)
                    form = StaffForm(instance=staff)  # Populate the form with the staff details
                    return render(request, 'accounts/add_staff.html', {'form': form, 'staff': staff})
                except User.DoesNotExist:
                    messages.error(request, 'No staff found with that email.')

        elif action == 'delete':
            if search_query:
                try:
                    staff = User.objects.get(email=search_query)
                    staff.delete()
                    messages.success(request, 'Staff deleted successfully.')
                    return redirect('accounts:add_staff')  # Redirect to clear the form and messages
                except User.DoesNotExist:
                    messages.error(request, 'Staff not found.')

        elif action == 'add':
            form = StaffForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Staff added successfully.')
                return redirect('accounts:add_staff')  # Redirect to clear the form and messages
            else:
                messages.error(request, 'Error in form submission.')
                # Debugging info
                print("Form errors:", form.errors)  # Print form errors to console/log

    # Handle GET request and initial display
    if form is None:
        form = StaffForm()

    return render(request, 'accounts/add_staff.html', {'form': form})

def list_patients(request):
    patients = User.objects.filter(is_staff=False).select_related('problem')  # Fetch related Problem data
    return render(request, 'accounts/patients_list.html', {'patients': patients})

def patient_detail(request, patient_id):
    patient = get_object_or_404(User, pk=patient_id, is_staff=False)
    problem = Problem.objects.filter(user=patient).first()  # Fetch related Problem data
    bookings = Booking.objects.filter(user=patient).order_by('date', 'time')
    return render(request, 'accounts/patient_detail.html', {'patient': patient, 'problem': problem, 'bookings': bookings})

def delete_patient(request, patient_id):
    patient = get_object_or_404(User, id=patient_id, is_staff=False)

    # Delete associated problem if exists
    if hasattr(patient, 'problem'):
        patient.problem.delete()

    # Delete all bookings associated with the patient
    Booking.objects.filter(user=patient).delete()

    # Delete the patient
    patient.delete()

    messages.success(request, 'Patient and associated records have been deleted.')
    return redirect('accounts:patients_list')
