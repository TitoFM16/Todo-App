from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseBadRequest,HttpResponse
from .models import Task
from .forms import TaskForm
from django.core.serializers import serialize
from django.core.serializers.json import Serializer as JsonSerializer
from django.views.decorators.csrf import csrf_exempt
# def task_list(request):
#     tasks = Task.objects.all().order_by('due_date', 'priority')
#     return render(request, 'todo/task_list.html', {'tasks': tasks})
def task_list(request):
    tasks = Task.objects.filter(completed=False).order_by('due_date', 'priority')
    return render(request, 'todo/task_list.html', {'tasks': tasks})

class TaskSerializer(JsonSerializer):
    def get_dump_object(self, obj):
        dump_object = super().get_dump_object(obj)
        dump_object['id'] = obj.pk
        return dump_object
def get_ordered_tasks(request):
    tasks = Task.objects.filter(completed=False).order_by('due_date', 'priority')
    serialized_tasks = serialize('json', tasks)
    return JsonResponse(serialized_tasks, safe=False)

# def get_ordered_tasks(request):
#     tasks = Task.objects.filter(completed=False).order_by('due_date', ('priority'))
#     serialized_tasks = TaskSerializer().serialize(tasks)
#     return JsonResponse(serialized_tasks, safe=False)

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
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             task = form.save()
#             # return JsonResponse({'id': task.id, 'title': task.title, 'description': task.description, 'due_date': task.due_date.strftime('%Y-%m-%d %H:%M:%S'), 'priority': task.get_priority_display()})
#         return HttpResponse("")
#     else:
#         form = TaskForm()
#     return render(request, 'todo/', {'form': form})

def task_create_modal(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            response_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date.strftime('%Y-%m-%d %H:%M:%S'),
                'priority': task.get_priority_display(),
            }
            return JsonResponse(response_data)
        else:
            # If the form is not valid, return the errors as JSON
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
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
    if request.method == 'DELETE':
        task.delete()
        data = {"success":True}
        return JsonResponse(data)
    elif request.method == 'GET':
        task.delete()
        return redirect('todo:completed_tasks')
    else:
        print("request.methos",request.method)
        data = {"success":False}
        return JsonResponse(data)



def completed_tasks(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        task.completed = True
        task.save()
        completed_tasks = Task.objects.filter(completed=True).order_by('due_date', 'priority')
        return render(request, 'todo/completed_tasks.html', {'completed_tasks': completed_tasks})
    elif request.method =='GET':
        completed_tasks = Task.objects.filter(completed=True).order_by('due_date', 'priority')
        return render(request, 'todo/completed_tasks.html', {'completed_tasks': completed_tasks})
    
def undo_completed_tasks(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        task.completed = False
        task.save()
        completed_tasks = Task.objects.filter(completed=True).order_by('due_date', 'priority')
        return render(request, 'todo/completed_tasks.html', {'completed_tasks': completed_tasks})
    elif request.method =='GET':
        completed_tasks = Task.objects.filter(completed=True).order_by('due_date', 'priority')
        return render(request, 'todo/completed_tasks.html', {'completed_tasks': completed_tasks})


