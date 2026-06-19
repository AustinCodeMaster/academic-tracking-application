from django.contrib import admin
from .models import LearnerProfile, Competency, AssessmentTask, AssessmentResult

admin.site.register(LearnerProfile)
admin.site.register(Competency)
admin.site.register(AssessmentTask)
admin.site.register(AssessmentResult)
