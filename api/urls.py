from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("taskList",views.taskList,name="taskList"),
    path("projectList",views.projectList,name="projectList"),
]