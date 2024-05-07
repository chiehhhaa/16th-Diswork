from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, get_list_or_404
from .models import Task
from random import randint, choice
from django.views.decorators.http import require_POST

# Create your views here.

def index(req):
    tasks = get_list_or_404(Task)
    
    return render(req, 'tasks/index.html', {'tasks':tasks})

def new(req):
    return render(req, 'tasks/new.html')

@require_POST
def create(req):
    name_list = ['joe', 'john', 'may', 'mary']
    # print(req.POST['get_time'])
    # print(req.POST['start_time'])
    # print(req.POST['end_time'])
    task = Task(
        created_user=choice(name_list),
        title=req.POST['title'],
        content=req.POST['content'],
        get_time=req.POST['get_time'],
        start_time=req.POST['start_time'],
        end_time=req.POST['end_time'],
    )
    task.save()

    return HttpResponse('created is ok', task)

def show(req, pk):
    task = get_object_or_404(Task, pk=pk)

    if req.method == 'POST':
        task.title=req.POST['title']
        task.content=req.POST['content']
        task.get_time=req.POST['get_time']
        task.start_time=req.POST['start_time']
        task.end_time=req.POST['end_time']
        task.save()

        return redirect('tasks:show', pk=task.id)

    return render(req, 'tasks/show.html', {'task':task})

def edit(req, pk):
    task = get_object_or_404(Task, pk=pk)
   
    return render(req, 'tasks/edit.html', {'task':task})


@require_POST
def delete(req, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
   
    return HttpResponse('')

