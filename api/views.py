from django.shortcuts import render
from .models import Task,Projects
from django.http import JsonResponse
# Create your views here.
def index(request):
    return render(request,'api/index.html')

def taskList(request):
    if request.method=='POST':
        taskName=request.POST['taskName']
        taskDescription=request.POST['taskDescription']
        dueDate=request.POST['dueDate']
        isPriority=request.POST['isPriority']
        user=request.user
        task=Task.objects.create(taskName,taskDescription,dueDate,isPriority,user)
        task.save()
    else:
        tasks=Task.objects.all()
        tasks=tasks.order_by("-timestamp").all()
        return JsonResponse([task.serialize() for task in tasks],safe=False)

def projectList(request):
    projects=Projects.objects.all()
    projects=projects.order_by("-timestamp").all()
    return JsonResponse([project.serialize()for project in projects],safe=False)