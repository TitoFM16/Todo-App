from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseBadRequest
from .models import Task
from .forms import TaskForm

# def task_list(request):
#     tasks = Task.objects.all().order_by('due_date', 'priority')
#     return render(request, 'todo/task_list.html', {'tasks': tasks})
def task_list(request):
    tasks = Task.objects.filter(completed=False).order_by('due_date', 'priority')
    return render(request, 'todo/task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'todo/task_detail.html', {'task': task})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('/task/' + str(task.pk))
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form})

# def task_create_modal(request):
#     form = TaskForm(request.POST or None, instance=Task())
#     context = {'form': form}
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('todo:task_list')
#     return render(request, 'todo/task_create_modal.html', context)
def task_create_modal(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('/')
            # return redirect('/task/' + str(task.pk))
    else:
        form = TaskForm()
    return render(request, 'todo/task_create_modal.html', {'form': form})

def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todo:task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('todo:task_list')
    return render(request, 'todo/task_confirm_delete.html', {'task': task})

def completed_tasks(request):
    completed_tasks = Task.objects.filter(completed=True).order_by('due_date', 'priority')
    return render(request, 'todo/completed_tasks.html', {'completed_tasks': completed_tasks})

# def completed_tasks(request):
#     if request.method == 'POST':
#         task_id = request.POST.get('task_id')
#         task = Task.objects.get(id=task_id)
#         task.completed = True
#         task.save()
#         return redirect('todo:task_list')
#     return render(request, 'todo/completed_tasks.html', {'tasks': completed_tasks})

# def index(request):
#     tasks = Task.objects.filter(completed=False).order_by('due_date', '-priority')
#     completed_tasks = Task.objects.filter(completed=True).order_by('-due_date', 'priority')
#     return render(request, 'todo/index.html', {'tasks': tasks, 'completed_tasks': completed_tasks})
