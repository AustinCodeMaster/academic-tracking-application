from django.db import models
from django.conf import settings

class LearnerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learner_profile')
    admission_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')))
    class_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.full_name} ({self.admission_number})"

class Competency(models.Model):
    competency_code = models.CharField(max_length=20, unique=True)
    competency_name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_competencies', 
        limit_choices_to={'role': 'Teacher'}
    )

    def __str__(self):
        return f"{self.competency_code}: {self.competency_name}"

class AssessmentTask(models.Model):
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE, related_name='tasks')
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_tasks', 
        limit_choices_to={'role': 'Teacher'}
    )
    task_title = models.CharField(max_length=100)
    task_description = models.TextField()
    task_date = models.DateField()

    def __str__(self):
        return self.task_title

class AssessmentResult(models.Model):
    learner = models.ForeignKey(LearnerProfile, on_delete=models.CASCADE, related_name='results')
    task = models.ForeignKey(AssessmentTask, on_delete=models.CASCADE, related_name='results')
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='recorded_results', 
        limit_choices_to={'role': 'Teacher'}
    )
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rating = models.CharField(max_length=30)
    feedback = models.TextField()
    assessment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.learner.full_name} - {self.task.task_title}"

