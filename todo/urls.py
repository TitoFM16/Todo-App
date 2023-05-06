from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('completed/', views.completed_tasks, name='completed_tasks'),
    path('new/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_edit, name='edit_task'),
    path('delete/<int:pk>/', views.task_delete, name='delete_task'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task_create_modal/', views.task_create_modal, name='task_create_modal'),
]
