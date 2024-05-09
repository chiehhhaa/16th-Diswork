from django.shortcuts import render, HttpResponse
from .models import Task

# Create your views here.

def index(req):
    return HttpResponse('index')

def new(req):
    return HttpResponse('new')

def create(req):
    task = Task(
        created_user_name=req.POST['created_user_name'],
        title=req.POST['title'],
        content=req.POST['content'],
        start_time=req.POST['start_time'],
        end_time=req.POST['end_time'],
    )
    task.save()

    return HttpResponse('created is ok', task)

def show(req, pk):
    return HttpResponse('show')

def edit(req, pk):
    return HttpResponse('edit')

def delete(req, pk):
    return HttpResponse('delete')

