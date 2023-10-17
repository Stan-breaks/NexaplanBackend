from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="task_user")
    taskName=models.CharField(max_length=200)
    taskDescription=models.CharField(max_length=200)
    isPriority=models.BooleanField()
    done=models.BooleanField(default=False)
    timestamp=models.DateField(auto_now_add=True)
    dueDate=models.DateField()
    def serialize(self):
        return{
            'user':self.user,
            'taskName':self.taskName,
            'taskDescription':self.taskDescription,
            'isPriority':self.isPriority,
            'done':self.done,
            'timestamp':self.timestamp.strftime('%b %d %Y, %I:%M %p'),
            'dueDate':self.dueDate.strftime('%b %d %Y, %I:%M %p'),
        }


class Projects(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="project_user")
    projectName=models.CharField(max_length=200)
    projectTask=models.ManyToManyField(Task,blank=False,related_name='project_tasks')
    projectStatus=models.BooleanField(default=True)
    timestamp=models.DateTimeField(auto_now_add=True)
