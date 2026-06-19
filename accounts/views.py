from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from students.models import LearnerProfile

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role == role:
                login(request, user)
                if role == 'Administrator':
                    return redirect('admin_dashboard')
                elif role == 'Teacher':
                    return redirect('teacher_dashboard')
                elif role == 'Learner':
                    return redirect('learner_dashboard')
            else:
                messages.error(request, 'Role does not match your account.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')

@login_required
def admin_dashboard(request):
    if request.user.role != 'Administrator':
        return redirect('login')
    return render(request, 'accounts/admin_dashboard.html')

@login_required
def teacher_dashboard(request):
    if request.user.role != 'Teacher':
        return redirect('login')
    return render(request, 'accounts/teacher_dashboard.html')

@login_required
def learner_dashboard(request):
    if request.user.role != 'Learner':
        return redirect('login')
    
    try:
        profile = request.user.learner_profile
        results = profile.results.all().order_by('-assessment_date')
    except LearnerProfile.DoesNotExist:
        profile = None
        results = []
        
    return render(request, 'accounts/learner_dashboard.html', {'profile': profile, 'results': results})
