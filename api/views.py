from django.shortcuts import render
from .models import Task,Project,User
from django.http import JsonResponse
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
# Create your views here.

def index(request):
    return render(request,'api/index.html')

@csrf_exempt
def register(request):
    data=json.loads(request.body)

    userName=data['userName']
    email=data['email']
    password=data['password']

    try:
        user=User.objects.create_user(userName,email,password)
        user.save()
        return JsonResponse({'message':'register success','user':userName})
    except IntegrityError:
        return JsonResponse({'message':'Account already exist'})

@csrf_exempt
def login(request):
    if request.method =='POST':
        data = json.loads(request.body)
        email=data['email']
        password=data['password']
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                return JsonResponse({'message': 'login success','user':user.username})
            else:
                return JsonResponse({'message': 'login failure'})
                
        except User.DoesNotExist:
            return JsonResponse({'message': 'User does not exist'})
    else:
        return JsonResponse({'message': 'Invalid request method'})

@csrf_exempt
def taskList(request):
    if request.method=='POST':
        data=json.loads(request.body)
        taskName=data['taskName']
        taskDescription=data['taskDescription']
        dueDate=data['dueDate']
        isPriority=data['isPriority']
        done=data["done"]
        userName=data["user"]
        User=get_user_model()
        try:
            user = User.objects.get(username=userName)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        task = Task.objects.create(taskName=taskName,taskDescription=taskDescription,dueDate=dueDate,isPriority=isPriority,user=user,done=done)
        task.save()
        return JsonResponse({'message':'add task success'})
    else:
        userName=request.GET.get('user')
        User=get_user_model()
        user=User.objects.get(username=userName)
        tasks = Task.objects.filter(user=user)
        tasks=tasks.order_by("-timestamp").all()
        return JsonResponse([task.serialize() for task in tasks],safe=False)

def taskView(request):
    taskId=request.GET.get('id')
    task=Task.objects.get(id=taskId)
    return JsonResponse(task.serialize())

@csrf_exempt
def completeTask(request,taskId):
    if request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.get(id=taskId)
        task.done = True
        task.save()
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def deleteTask(request,taskId):
    if request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.get(id=taskId)
        task.delete()
        return JsonResponse({'status':'success'},status=200)
    else:
        return JsonResponse({'error':'Invalid request'},status=400)  

@csrf_exempt
def projectList(request):
    if request.method=='POST':
        data=json.loads(request.body)
        projectName=data["name"]
        projectDescription=data["description"]
        userName=data["user"]
        User=get_user_model()
        try:
           user=User.objects.get(username=userName)
        except ObjectDoesNotExist:
            return JsonResponse({'error':'user not found'},status=400)
        project=Project.objects.create(projectName=projectName,projectDescription=projectDescription,user=user)
        project.save()
        return JsonResponse({'message':'project added successfully'})
    else:
        userName=request.GET.get('user')
        User=get_user_model()
        user=User.objects.get(username=userName)
        projects=Project.objects.filter(user=user)
        projects=projects.order_by("-timestamp").all()
        return JsonResponse([project.serialize()for project in projects],safe=False)
    
def dashboard(request):
    userName=request.GET.get('user')
    User=get_user_model()
    user=User.objects.get(username=userName)
    totalTasks=Task.objects.filter(user=user).count()
    totalProjects=Project.objects.filter(user=user).count()
    completedTasks=Task.objects.filter(user=user,done=True).count()
    pendingTasks=Task.objects.filter(user=user,done=False).count()
    activeProjects=Project.objects.filter(user=user,projectStatus=True).count()
    return JsonResponse({'totalTasks':totalTasks,'completedTasks':completedTasks,'pendingTasks':pendingTasks,'totalProjects':totalProjects,'activeProjects':activeProjects},safe=False)

def projectView(request,projectId):
    project=Project.objects.get(id=projectId)
    return JsonResponse(project.serialize(),safe=False)

def usersList(request):
    if request.method=='POST':
        data=json.loads(request.body)
        userName=data['userName']
        
    User=get_user_model()
    users=User.objects.all()
    usernames = [user.username for user in users]
    return JsonResponse(usernames,safe=False)

@csrf_exempt
def projectTasks(request,projectId):
    if request.method=='POST':
        data=json.loads(request.body)
        taskName=data['taskName']
        taskDescription=data['taskDescription']
        assignedTo=data['assignedTo']
        dueDate=data['dueDate']
        isPriority=data['isPriority']
        done=data["done"]
        projectId=data["projectId"]

        project=Project.objects.get(id=projectId)
        User=get_user_model()
        try:
            user=User.objects.get(username=assignedTo)
        except ObjectDoesNotExist:
            return JsonResponse({'error':'user not found'},status=400)
        
        task=Task.objects.create(taskName=taskName,user=user,taskDescription=taskDescription,dueDate=dueDate,isPriority=isPriority,project=project,done=done)
        task.save()
        project.projectTasks.add(task)
        return JsonResponse({'message':'add task success'})