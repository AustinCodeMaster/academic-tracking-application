from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]