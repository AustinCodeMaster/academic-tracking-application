from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('portal/admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('learner/dashboard/', views.learner_dashboard, name='learner_dashboard'),
]