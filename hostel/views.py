from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.http import JsonResponse
from .models import Student, HostelApplication, Hostel, University, Room
from .forms import (UserRegistrationForm, StudentProfileForm, HostelApplicationForm,UniversityRegistrationForm, HostelForm, RoomForm)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            if hasattr(user, 'university_admin'):
                return redirect('university_dashboard')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'hostel/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def home(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'university_admin'):
            return redirect('university_dashboard')
        return redirect('dashboard')
    return render(request, 'hostel/home.html')

def is_university_admin(user):
    return hasattr(user, 'university_admin')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        student_form = StudentProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please wait for the verification set by the office.')
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()
        student_form = StudentProfileForm()
    
    return render(request, 'hostel/register.html',{'user_form': user_form,'student_form': student_form})

def register_university(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        university_form = UniversityRegistrationForm(request.POST, request.FILES)
        
        if user_form.is_valid() and university_form.is_valid():
            user = user_form.save()
            university = university_form.save(commit=False)
            university.admin_user = user
            university.save()
            login(request, user)
            messages.success(request, 'University registration successful! Please wait for admin verification.')
            return redirect('university_dashboard')
    else:
        user_form = UserRegistrationForm()
        university_form = UniversityRegistrationForm()
    return render(request, 'hostel/register_university.html',{'user_form': user_form,'university_form': university_form})

@login_required
@user_passes_test(is_university_admin)
def university_dashboard(request):
    university = request.user.university_admin
    hostels = Hostel.objects.filter(university=university)
    return render(request, 'hostel/university_dashboard.html',{'university': university,'hostels': hostels})

@login_required
@user_passes_test(is_university_admin)
def manage_hostel(request, hostel_id=None):
    university = request.user.university_admin
    hostel = None
    if hostel_id:
        hostel = get_object_or_404(Hostel, id=hostel_id, university=university)
    if request.method == 'POST':
        form = HostelForm(request.POST, instance=hostel)
        if form.is_valid():
            hostel = form.save(commit=False)
            hostel.university = university
            hostel.save()
            messages.success(request, 'Hostel saved successfully!')
            return redirect('university_dashboard')
    else:
        form = HostelForm(instance=hostel)
    return render(request, 'hostel/manage_hostel.html',{'form': form,'hostel': hostel})

@login_required
@user_passes_test(is_university_admin)
def manage_room(request, hostel_id, room_id=None):
    university = request.user.university_admin
    hostel = get_object_or_404(Hostel, id=hostel_id, university=university)
    room = None
    if room_id:
        room = get_object_or_404(Room, id=room_id, hostel=hostel)  
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save(commit=False)
            room.hostel = hostel
            room.save()
            messages.success(request, 'Room saved successfully!')
            return redirect('view_hostel', hostel_id=hostel.id)
    else:
        form = RoomForm(instance=room)
    return render(request,'hostel/manage_room.html',{'form': form,'room': room,'hostel': hostel})

@login_required
@user_passes_test(is_university_admin)
def view_hostel(request, hostel_id):
    university = request.user.university_admin
    hostel = get_object_or_404(Hostel, id=hostel_id, university=university)
    rooms = Room.objects.filter(hostel=hostel)
    return render(request,'hostel/view_hostel.html',{'hostel': hostel,'rooms': rooms})

@login_required
def dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        applications = HostelApplication.objects.filter(student=student)
        return render(request, 'hostel/dashboard.html',{'student': student,'applications': applications})
    except Student.DoesNotExist:
        return redirect('register')

@login_required
def apply_hostel(request):
    try:
        student = Student.objects.get(user=request.user)
        if not student.is_verified:
            messages.warning(request, 'Your account is not verified yet. Please wait for admin verification.')
            return redirect('dashboard')
        
        if request.method == 'POST':
            form = HostelApplicationForm(request.POST, student=student)
            if form.is_valid():
                application = form.save(commit=False)
                application.student = student
                application.save()
                if application.room:
                    room = application.room
                    room.available_capacity -= 1
                    room.save()
                messages.success(request, 'Application submitted successfully!')
                return redirect('dashboard')
        else:
            form = HostelApplicationForm(student=student)
        return render(request, 'hostel/apply_hostel.html', {'form': form})
    except Student.DoesNotExist:
        return redirect('register')

@login_required
def application_status(request, application_id):
    application = get_object_or_404(HostelApplication, id=application_id, student__user=request.user)
    return render(request, 'hostel/application_status.html', {'application': application})

@login_required
def load_rooms(request):
    hostel_id = request.GET.get('hostel')
    rooms = Room.objects.filter(hostel_id=hostel_id, available_capacity__gt=0)
    data = [{'id': room.id, 'room_number': room.room_number, 'room_type': room.room_type, 'available_capacity': room.available_capacity} for room in rooms]
    return JsonResponse(data, safe=False)
