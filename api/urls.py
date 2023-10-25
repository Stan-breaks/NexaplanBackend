from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("login",views.login,name="login"),
    path("register",views.register,name="register"),
    path("taskList",views.taskList,name="taskList"),
    path("taskView",views.taskView,name="taskView"),
    path("projectList",views.projectList,name="projectList"),
    path("completeTask/<int:taskId>",views.completeTask,name="completeTask"),
    path("deleteTask/<int:taskId>",views.deleteTask,name="deleteTask")
]