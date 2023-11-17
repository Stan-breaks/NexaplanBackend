from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("login",views.login,name="login"),
    path("register",views.register,name="register"),
    path("taskList",views.taskList,name="taskList"),
    path("categoryList",views.categoryList,name="categoryList"),
    path("taskCategories",views.taskCategories,name="taskCategories"),
    path("taskView",views.taskView,name="taskView"),
    path("projectList",views.projectList,name="projectList"),
    path("collaboratorsProjectList",views.collaboratorsProjectList,name="collaboratorsProjectList"),
    path("projectView/<int:projectId>",views.projectView,name="projectView"),
    path("projectHandling/<int:projectId>",views.projectHandling,name="projectHandling"),
    path("completeTask/<int:taskId>",views.completeTask,name="completeTask"),
    path("deleteTask/<int:taskId>",views.deleteTask,name="deleteTask"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("usersList/<int:projectId>",views.usersList,name="usersList"),
    path("projectCollaborators/<int:projectId>",views.projectCollaborators,name="projectCollaborators"),
    path("projectTasks/<int:projectId>",views.projectTasks,name="projectTasks"),
    path("search",views.search,name="search"),
]