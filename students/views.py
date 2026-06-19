from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LearnerProfile, Competency, AssessmentTask, AssessmentResult
from accounts.models import CustomUser

# --- LEARNER MANAGEMENT (Teacher only) ---

@login_required
def learner_list(request):
    if request.user.role != 'Teacher':
        return redirect('login')
    learners = LearnerProfile.objects.all().order_by('full_name')
    return render(request, 'students/learner_list.html', {'learners': learners})

@login_required
def learner_create(request):
    if request.user.role != 'Teacher':
        return redirect('login')
    
    # Needs a list of available learner users who don't have a profile yet
    available_users = CustomUser.objects.filter(role='Learner', learner_profile__isnull=True)
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        admission_number = request.POST.get('admission_number')
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        class_name = request.POST.get('class_name')
        date_of_birth = request.POST.get('date_of_birth')

        if not all([user_id, admission_number, full_name, gender, class_name, date_of_birth]):
            messages.error(request, 'All fields are required.')
        else:
            try:
                user = CustomUser.objects.get(id=user_id)
                LearnerProfile.objects.create(
                    user=user,
                    admission_number=admission_number,
                    full_name=full_name,
                    gender=gender,
                    class_name=class_name,
                    date_of_birth=date_of_birth
                )
                messages.success(request, 'Learner profile created successfully.')
                return redirect('learner_list')
            except Exception as e:
                messages.error(request, f'Error creating Learner: {str(e)}')

    return render(request, 'students/learner_form.html', {'available_users': available_users})

@login_required
def learner_update(request, pk):
    if request.user.role != 'Teacher':
        return redirect('login')
    
    learner = get_object_or_404(LearnerProfile, pk=pk)
    
    if request.method == 'POST':
        learner.admission_number = request.POST.get('admission_number')
        learner.full_name = request.POST.get('full_name')
        learner.gender = request.POST.get('gender')
        learner.class_name = request.POST.get('class_name')
        learner.date_of_birth = request.POST.get('date_of_birth')
        learner.save()
        messages.success(request, 'Learner profile updated successfully.')
        return redirect('learner_list')

    return render(request, 'students/learner_form.html', {'learner': learner})

@login_required
def learner_delete(request, pk):
    if request.user.role != 'Teacher':
        return redirect('login')
    
    learner = get_object_or_404(LearnerProfile, pk=pk)
    if request.method == 'POST':
        learner.delete()
        messages.success(request, 'Learner profile deleted successfully.')
        return redirect('learner_list')
        
    return render(request, 'students/learner_confirm_delete.html', {'learner': learner})

# --- COMPETENCY MANAGEMENT (Teacher only) ---

@login_required
def competency_list(request):
    if request.user.role != 'Teacher':
        return redirect('login')
    competencies = Competency.objects.all().order_by('competency_code')
    return render(request, 'students/competency_list.html', {'competencies': competencies})

@login_required
def competency_create(request):
    if request.user.role != 'Teacher':
        return redirect('login')
    
    if request.method == 'POST':
        competency_code = request.POST.get('competency_code')
        competency_name = request.POST.get('competency_name')
        description = request.POST.get('description')

        if not all([competency_code, competency_name, description]):
            messages.error(request, 'All fields are required.')
        elif Competency.objects.filter(competency_code=competency_code).exists():
            messages.error(request, 'A competency with this code already exists.')
        else:
            Competency.objects.create(
                competency_code=competency_code,
                competency_name=competency_name,
                description=description,
                created_by=request.user
            )
            messages.success(request, 'Competency created successfully.')
            return redirect('competency_list')

    return render(request, 'students/competency_form.html')

@login_required
def competency_update(request, pk):
    if request.user.role != 'Teacher':
        return redirect('login')
    
    competency = get_object_or_404(Competency, pk=pk)
    
    if request.method == 'POST':
        competency_code = request.POST.get('competency_code')
        
        # Check uniqueness, ignoring the current object
        if Competency.objects.filter(competency_code=competency_code).exclude(pk=pk).exists():
            messages.error(request, 'A competency with this code already exists.')
        else:
            competency.competency_code = competency_code
            competency.competency_name = request.POST.get('competency_name')
            competency.description = request.POST.get('description')
            competency.save()
            messages.success(request, 'Competency updated successfully.')
            return redirect('competency_list')

    return render(request, 'students/competency_form.html', {'competency': competency})

@login_required
def competency_delete(request, pk):
    if request.user.role != 'Teacher':
        return redirect('login')
    
    competency = get_object_or_404(Competency, pk=pk)
    if request.method == 'POST':
        competency.delete()
        messages.success(request, 'Competency deleted successfully.')
        return redirect('competency_list')
        
    return render(request, 'students/competency_confirm_delete.html', {'competency': competency})

# --- ASSESSMENT TASK MANAGEMENT (Teacher only) ---

@login_required
def task_list(request):
    if request.user.role != 'Teacher':
        return redirect('login')
    tasks = AssessmentTask.objects.all().order_by('-task_date')
    return render(request, 'students/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.user.role != 'Teacher':
        return redirect('login')
    
    competencies = Competency.objects.all()
    
    if request.method == 'POST':
        competency_id = request.POST.get('competency_id')
        task_title = request.POST.get('task_title')
        task_description = request.POST.get('task_description')
        task_date = request.POST.get('task_date')

        if not all([competency_id, task_title, task_description, task_date]):
            messages.error(request, 'All fields are required.')
        else:
            try:
                competency = Competency.objects.get(id=competency_id)
                AssessmentTask.objects.create(
                    competency=competency,
                    teacher=request.user,
                    task_title=task_title,
                    task_description=task_description,
                    task_date=task_date
                )
                messages.success(request, 'Assessment Task created successfully.')
                return redirect('task_list')
            except Exception as e:
                messages.error(request, f'Error creating Task: {str(e)}')

    return render(request, 'students/task_form.html', {'competencies': competencies})

@login_required
def task_update(request, pk):
    if request.user.role != 'Teacher':
        return redirect('login')
    
    task = get_object_or_404(AssessmentTask, pk=pk)
    competencies = Competency.objects.all()
    
    if request.method == 'POST':
        competency_id = request.POST.get('competency_id')
        try:
            competency = Competency.objects.get(id=competency_id)
            task.competency = competency
            task.task_title = request.POST.get('task_title')
            task.task_description = request.POST.get('task_description')
            task.task_date = request.POST.get('task_date')
            task.save()
            messages.success(request, 'Assessment Task updated successfully.')
            return redirect('task_list')
        except Exception as e:
            messages.error(request, f'Error updating Task: {str(e)}')

    return render(request, 'students/task_form.html', {'task': task, 'competencies': competencies})

@login_required
def task_delete(request, pk):
    if request.user.role != 'Teacher':
        return redirect('login')
    
    task = get_object_or_404(AssessmentTask, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Assessment Task deleted successfully.')
        return redirect('task_list')
        
    return render(request, 'students/task_confirm_delete.html', {'task': task})

# --- ASSESSMENT RESULT MANAGEMENT (Teacher only) ---

@login_required
def result_list(request):
    if request.user.role != 'Teacher':
        return redirect('login')
    results = AssessmentResult.objects.all().order_by('-assessment_date')
    return render(request, 'students/result_list.html', {'results': results})

@login_required
def result_create(request):
    if request.user.role != 'Teacher':
        return redirect('login')
    
    learners = LearnerProfile.objects.all().order_by('full_name')
    tasks = AssessmentTask.objects.all().order_by('-task_date')
    
    if request.method == 'POST':
        learner_id = request.POST.get('learner_id')
        task_id = request.POST.get('task_id')
        score = request.POST.get('score') or None
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')

        if not all([learner_id, task_id, rating, feedback]):
            messages.error(request, 'Learner, Task, Rating, and Feedback are required fields.')
        else:
            try:
                learner = LearnerProfile.objects.get(id=learner_id)
                task = AssessmentTask.objects.get(id=task_id)
                AssessmentResult.objects.create(
                    learner=learner,
                    task=task,
                    teacher=request.user,
                    score=score,
                    rating=rating,
                    feedback=feedback
                )
                messages.success(request, 'Assessment Result recorded successfully.')
                return redirect('result_list')
            except Exception as e:
                messages.error(request, f'Error recording result: {str(e)}')

    return render(request, 'students/result_form.html', {'learners': learners, 'tasks': tasks})

@login_required
def result_update(request, pk):
    if request.user.role != 'Teacher':
        return redirect('login')
    
    result = get_object_or_404(AssessmentResult, pk=pk)
    learners = LearnerProfile.objects.all().order_by('full_name')
    tasks = AssessmentTask.objects.all().order_by('-task_date')
    
    if request.method == 'POST':
        learner_id = request.POST.get('learner_id')
        task_id = request.POST.get('task_id')
        score = request.POST.get('score') or None
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')

        try:
            result.learner = LearnerProfile.objects.get(id=learner_id)
            result.task = AssessmentTask.objects.get(id=task_id)
            result.score = score
            result.rating = rating
            result.feedback = feedback
            result.save()
            messages.success(request, 'Assessment Result updated successfully.')
            return redirect('result_list')
        except Exception as e:
            messages.error(request, f'Error updating result: {str(e)}')

    return render(request, 'students/result_form.html', {'result': result, 'learners': learners, 'tasks': tasks})

@login_required
def result_delete(request, pk):
    if request.user.role != 'Teacher':
        return redirect('login')
    
    result = get_object_or_404(AssessmentResult, pk=pk)
    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Assessment Result deleted successfully.')
        return redirect('result_list')
        
    return render(request, 'students/result_confirm_delete.html', {'result': result})

# --- REPORTS MANAGEMENT (Teacher only) ---

@login_required
def report_view(request):
    if request.user.role != 'Teacher':
        return redirect('login')
    
    # Base queryset
    results = AssessmentResult.objects.all().select_related('learner', 'task__competency', 'teacher').order_by('-assessment_date')
    
    # Setup filter data
    tasks = AssessmentTask.objects.all()
    competencies = Competency.objects.all()
    ratings = [
        'Exceeding Expectations',
        'Meeting Expectations',
        'Approaching Expectations',
        'Below Expectations'
    ]
    
    # Process filters
    task_id = request.GET.get('task_id')
    competency_id = request.GET.get('competency_id')
    rating = request.GET.get('rating')
    
    if task_id:
        results = results.filter(task_id=task_id)
    if competency_id:
        results = results.filter(task__competency_id=competency_id)
    if rating:
        results = results.filter(rating=rating)
        
    context = {
        'results': results,
        'tasks': tasks,
        'competencies': competencies,
        'ratings': ratings,
        'selected_task': task_id,
        'selected_competency': competency_id,
        'selected_rating': rating,
    }
    
    return render(request, 'students/report.html', context)

