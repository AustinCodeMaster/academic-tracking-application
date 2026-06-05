from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.role == role:
                login(request, user)
                if role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('teacher_dashboard')
            else:
                messages.error(request, 'Role does not match your account.')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')


def teacher_dashboard(request):
    return render(request, 'accounts/teacher_dashboard.html')


def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')