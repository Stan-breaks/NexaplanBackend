from django.shortcuts import render
from .models import Task, Project, User, Comment
from django.http import JsonResponse
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from datetime import datetime

# Create your views here.


def index(request):
    return render(request, "api/index.html")


@csrf_exempt
def register(request):
    data = json.loads(request.body)

    userName = data["userName"]
    email = data["email"]
    password = data["password"]

    try:
        user = User.objects.create_user(userName, email, password)
        user.save()
        return JsonResponse({"message": "register success", "user": userName})
    except IntegrityError:
        return JsonResponse({"message": "Account already exist"})


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data["email"]
        password = data["password"]
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                return JsonResponse({"message": "login success", "user": user.username})
            else:
                return JsonResponse({"message": "login failure"})

        except User.DoesNotExist:
            return JsonResponse({"message": "User does not exist"})
    else:
        return JsonResponse({"message": "Invalid request method"})


@csrf_exempt
def taskList(request):
    if request.method == "POST":
        data = json.loads(request.body)
        taskName = data["taskName"]
        taskDescription = data["taskDescription"]
        dueDate = data["dueDate"]
        isPriority = data["isPriority"]
        done = data["done"]
        category = data["category"]
        userName = data["user"]
        User = get_user_model()
        try:
            user = User.objects.get(username=userName)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        task = Task.objects.create(
            taskName=taskName,
            taskDescription=taskDescription,
            dueDate=dueDate,
            isPriority=isPriority,
            user=user,
            done=done,
            category=category,
        )
        task.save()
        return JsonResponse({"message": "add task success"})
    else:
        userName = request.GET.get("user")
        User = get_user_model()
        user = User.objects.get(username=userName)
        tasks = Task.objects.filter(user=user)
        tasks = tasks.order_by("-timestamp").all()
        return JsonResponse([task.serialize() for task in tasks], safe=False)


def taskView(request):
    taskId = request.GET.get("id")
    task = Task.objects.get(id=taskId)
    return JsonResponse(task.serialize())


@csrf_exempt
def completeTask(request, taskId):
    if request.method == "POST":
        data = json.loads(request.body)
        task = Task.objects.get(id=taskId)
        task.done = True
        task.save()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def deleteTask(request, taskId):
    if request.method == "POST":
        data = json.loads(request.body)
        task = Task.objects.get(id=taskId)
        task.delete()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


def taskCategories(request):
    userName = request.GET.get("user")
    category = request.GET.get("category")
    User = get_user_model()
    if category == "upcoming deadlines":
        user = User.objects.get(username=userName)
        tasks = Task.objects.filter(user=user, dueDate__gte=datetime.now())
        tasks = tasks.order_by("-timestamp").all()
        return JsonResponse([task.serialize() for task in tasks], safe=False)
    user = User.objects.get(username=userName)
    tasks = Task.objects.filter(user=user, category=category)
    tasks = tasks.order_by("-timestamp").all()
    return JsonResponse([task.serialize() for task in tasks], safe=False)


def categoryList(request):
    userName = request.GET.get("user")
    label = request.GET.get("label")
    User = get_user_model()
    user = User.objects.get(username=userName)
    if label == "project":
        tasks = Task.objects.filter(user=user, hasProject=True)
        tasks = tasks.order_by("-timestamp").all()
        categories = [task.category for task in tasks]
        categories = list(set(categories))
        return JsonResponse(categories, safe=False)
    else:
        tasks = Task.objects.filter(user=user, hasProject=False)
        tasks = tasks.order_by("-timestamp").all()
        categories = [task.category for task in tasks]
        categories += ["upcoming deadlines"]
        categories = list(set(categories))
        return JsonResponse(categories, safe=False)


@csrf_exempt
def projectList(request):
    if request.method == "POST":
        data = json.loads(request.body)
        projectName = data["name"]
        projectDescription = data["description"]
        userName = data["user"]
        User = get_user_model()
        try:
            user = User.objects.get(username=userName)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "user not found"}, status=400)
        project = Project.objects.create(
            projectName=projectName, projectDescription=projectDescription, user=user
        )
        project.save()
        return JsonResponse({"message": "project added successfully"})
    else:
        userName = request.GET.get("user")
        User = get_user_model()
        user = User.objects.get(username=userName)
        projects = Project.objects.filter(user=user)
        projects = projects.order_by("-timestamp").all()
        return JsonResponse([project.serialize() for project in projects], safe=False)


def collaboratorsProjectList(request):
    userName = request.GET.get("user")
    projects = Project.objects.filter(collaborators__username__contains=userName)
    projects = projects.order_by("-timestamp").all()
    return JsonResponse([project.serialize() for project in projects], safe=False)


def dashboard(request):
    userName = request.GET.get("user")
    User = get_user_model()
    user = User.objects.get(username=userName)
    totalTasks = Task.objects.filter(user=user).count()
    totalProjects = Project.objects.filter(user=user).count()
    completedTasks = Task.objects.filter(user=user, done=True).count()
    pendingTasks = Task.objects.filter(user=user, done=False).count()
    activeProjects = Project.objects.filter(user=user, projectStatus=True).count()
    priorityTasks = Task.objects.filter(user=user, isPriority=True).count()
    upcomingDeadlines = Task.objects.filter(
        user=user, dueDate__gte=datetime.now()
    ).count()

    return JsonResponse(
        {
            "totalTasks": totalTasks,
            "completedTasks": completedTasks,
            "pendingTasks": pendingTasks,
            "totalProjects": totalProjects,
            "activeProjects": activeProjects,
            "priorityTasks": priorityTasks,
            "upcomingDeadlines": upcomingDeadlines,
        },
        safe=False,
    )


def projectView(request, projectId):
    project = Project.objects.get(id=projectId)
    return JsonResponse(project.serialize(), safe=False)


def usersList(request, projectId):
    project = Project.objects.get(id=projectId)
    userName = project.user.username
    User = get_user_model()
    users = User.objects.all()
    usernames = [user.username for user in users]
    usernames = list(filter(lambda x: x != userName, usernames))
    return JsonResponse(usernames, safe=False)


@csrf_exempt
def projectTasks(request, projectId):
    if request.method == "POST":
        data = json.loads(request.body)
        taskName = data["name"]
        taskDescription = data["description"]
        assignedTo = data["assignedTo"]
        dueDate = data["dueDate"]
        isPriority = data["priority"]
        category = data["category"]
        project = Project.objects.get(id=projectId)
        User = get_user_model()
        try:
            user = User.objects.get(username=assignedTo)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "user not found"}, status=400)

        task = Task.objects.create(
            taskName=taskName,
            user=user,
            taskDescription=taskDescription,
            dueDate=dueDate,
            isPriority=isPriority,
            category=category,
            hasProject=True,
        )
        task.save()
        project.projectTask.add(task)
        return JsonResponse({"message": "add task success"})


@csrf_exempt
def projectHandling(request, projectId):
    if request.method == "POST":
        project = Project.objects.get(id=projectId)
        project.projectStatus = not project.projectStatus
        project.save()
        return JsonResponse({"message": "project status flipped successfully"})


@csrf_exempt
def projectCollaborators(request, projectId):
    if request.method == "POST":
        data = json.loads(request.body)
        userName = data["collaborator"]
        project = Project.objects.get(id=projectId)
        User = get_user_model()
        try:
            user = User.objects.get(username=userName)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "user not found"}, status=400)
        project.collaborators.add(user)
        return JsonResponse({"message": "add collaborator success"})


def search(request):
    try:
        userName = request.GET.get("user")
        searchText = request.GET.get("search")
        User = get_user_model()
        user = User.objects.get(username=userName)
        tasks = Task.objects.filter(user=user, taskName__icontains=searchText)
        projects = Project.objects.filter(user=user, projectName__icontains=searchText)
        return JsonResponse(
            [project.serialize() for project in projects]
            + [task.serialize() for task in tasks],
            safe=False,
        )
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task does not exist"}, status=404)
    except Project.DoesNotExist:
        return JsonResponse({"error": "Project does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def settings(request):
    if request.method == "POST":
        data = json.loads(request.body)
        userName = request.GET.get("user")
        User = get_user_model()
        user = User.objects.get(username=userName)
        user.username = data["username"]
        user.email = data["email"]
        user.set_password(data["password"])
        user.save()
        return JsonResponse({"message": "settings saved successfully"})
    else:
        userName = request.GET.get("user")
        User = get_user_model()
        user = User.objects.get(username=userName)
        return JsonResponse({"username": user.username, "email": user.email})


@csrf_exempt
def profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        userName = request.GET.get("user")
        User = get_user_model()
        user = User.objects.get(username=userName)
        user.profilePicture = data["profilePicture"]
        user.save()
        return JsonResponse({"message": "profile picture saved successfully"})
    else:
        userName = request.GET.get("user")
        User = get_user_model()
        user = User.objects.get(username=userName)
        return JsonResponse({"profilePicture": user.profilePicture})


@csrf_exempt
def comment(request):
    id = request.GET.get("id")
    project = Project.objects.get(id=id)
