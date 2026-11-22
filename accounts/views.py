from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import UserProfile

def register_view(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', '')

        if not all([first_name, last_name, username, email, password, confirm_password, role]):
            messages.error(request, 'All Fields Are Required!')
            return redirect('register')

        if role not in ['Job Seeker', 'Employer']:
            messages.error(request, 'Invalid Role Selected!')
            return redirect('register')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please Enter a Valid Email Address!')
            return redirect('register')

        if len(password) < 8:
            messages.error(request, 'Password Must Be At Least 8 Characters!')
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('register')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            role=role
        )

        messages.success(request, 'Registration successful!')
        return redirect('register')

    return render(request, 'register.html')


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Username and Password Are Required!')
            return redirect('login')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')

        else:
            messages.error(request, 'Invalid Username or Password!')
            return redirect('login')

    return render(request, 'login.html')


@login_required(login_url='login')
def dashboard_view(request):

    user_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    role = user_profile.role if user_profile else None

    return render(
        request,
        'dashboard.html',
        {'role': role}
    )

@login_required(login_url='login')
def logout_view(request):

    logout(request)

    messages.success(request, 'You have logged out successfully!')

    return redirect('login')


@login_required(login_url='login')
def my_profile_view(request):

    return render(request, 'my_profile.html')