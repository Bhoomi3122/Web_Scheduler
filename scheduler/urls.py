# scheduler/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('add/',views.add_schedule,name='add_schedule'),
    path('view/<int:schedule_id>/',views.view_schedule,name='view_schedule'),
    path('add-task/',views.add_task,name='add_task'),
    path('create-schedule/',views.create_schedule,name='create_schedule'),
    path('delete_task/<int:task_id>/',views.delete_task,name='delete_task'),
    path('complete_task/<int:task_id>/',views.complete_task,name='complete_task'),
    path('edit/<int:task_id>/', views.edit, name='edit'),  
]