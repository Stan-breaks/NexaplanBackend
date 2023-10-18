from django.shortcuts import render
from .models import Task,Projects,User
from django.http import JsonResponse
from django.contrib.auth import authenticate,get_user_model
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def index(request):
    return render(request,'api/index.html')

def register(request):
    data=json.loads(request.body)

    userName=data['userName']
    email=data['email']
    password=data['password']
    
    try:
        user=User.objects.create_user(userName,email,password)
        user.save()
        return JsonResponse({'message':'register success'})
    except IntegrityError:
        return JsonResponse({'message':'Account already exist'})

@csrf_exempt
def login(request):
    if request.method=='POST':
        data = json.loads(request.body)
        email=data['email']
        password=data['password']
        User = get_user_model()
        try:
            # Get the user with the given email
            user = User.objects.get(email=email)
            
            # Authenticate the user
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                return JsonResponse({'message': 'login success'})
            else:
                return JsonResponse({'message': 'login failure'})
                
        except User.DoesNotExist:
            return JsonResponse({'message': 'User does not exist'})
    else:
        return JsonResponse({'message': 'Invalid request method'})

def taskList(request):
    if request.method=='POST':
        data=json.loads(request.body)

        taskName=data['taskName']
        taskDescription=data['taskDescription']
        dueDate=data['dueDate']
        isPriority=data['isPriority']
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