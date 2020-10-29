from django.db import models
from djongo import models
from datetime import datetime
from bson.objectid import ObjectId
# Create your models here.

class FSI_user(models.Model):
    # _id = models.ObjectIdField()
    id = models.CharField(max_length=22, primary_key=True)
    username= models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    full_name= models.CharField(max_length=255)
    email = models.EmailField()
    token = models.CharField(max_length=255)
    phone = models.IntegerField()

    def __str__(self):
        return self.username or ''

class Project(models.Model):
    # _id = models.ObjectIdField()
    id = models.CharField(max_length=22, primary_key=True)
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(FSI_user, on_delete=models.CASCADE)
    create_at = models.DateTimeField(default=datetime.now())
    start_time = models.DateTimeField(default=datetime.now())
    end_time = models.DateTimeField(default=datetime.now())
    company = models.CharField(max_length=255)


    # def __str__(self):
    #     return self.project_name
    def __str__(self):
        return (self.project_name)

class Post(models.Model):
    # _id = models.ObjectIdField()
    id = models.CharField(max_length=22, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    num_likes = models.IntegerField()
    num_comments = models.IntegerField()
    num_shares = models.IntegerField()
    content = models.TextField()
    time_create = models.DateTimeField()
    

    def __str__(self):
        return self.content


class Comments(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_create = models.DateTimeField()
    content = models.TextField()
    num_likes = models.IntegerField()
    author = models.CharField(max_length=255)
    effect = models.CharField(max_length=40)

    def __str__(self):
        return self.content

