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
    category=models.CharField(max_length=200,default='category')
    hasProject=models.BooleanField(default=False)
    def serialize(self):
        return{
            'id':self.id,
            'user':self.user.username,
            'taskName':self.taskName,
            'taskDescription':self.taskDescription,
            'isPriority':self.isPriority,
            'done':self.done,
            'timestamp':self.timestamp.strftime('%b %d %Y, %I:%M %p'),
            'dueDate':self.dueDate.strftime('%b %d %Y, %I:%M %p'),
            'category':self.category
        }


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_user")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Project(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="project_user")
    projectName=models.CharField(max_length=200)
    projectDescription=models.CharField(max_length=200,default='description')
    projectTask=models.ManyToManyField(Task,related_name='project_tasks')
    collaborators=models.ManyToManyField(User,related_name='collaborators')
    projectStatus=models.BooleanField(default=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    comments=models.ManyToManyField(Comment,related_name='comments')
    def serialize(self):
        return{
            'id':self.id,
            'user':self.user.username,
            'projectName':self.projectName,
            'projectDescription':self.projectDescription,
            'projectTask':[task.taskName for task in self.projectTask.all()],
            'collaborators':[collaborator.username for collaborator in self.collaborators.all()],
            'projectStatus':self.projectStatus,
            'timestamp':self.timestamp,
        }
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile_user")
    profilePicture=models.ImageField(upload_to='profile_pictures',blank=True)

    def serialize(self):
        return{
            'id':self.id,
            'user':self.user.username,
            'profilePicture':self.profilePicture
        }

