from audioop import reverse
from distutils.command.upload import upload
from django.db import models
from django.forms import ImageField
from pkg_resources import to_filename
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.shortcuts import redirect, render



##Account

# class User(AbstractUser):
#     picture = models.CharField(default=None, blank=True, null=True, max_length=2000)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
    
#     def get_absolute_url(self):
#         return reverse('detail', kwargs = {'account_id': self.id})
    
#     def __str__(self):
#         return self.username

class Account(models.Model):
    picture = models.CharField(default='https://i.imgur.com/VKXouC4.png', blank=True, null=True, max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # likes = models.ManyToManyField(Comment)

    def get_absolute_url(self):
        return reverse('detail', kwargs = {'account_id': self.id})
    
    def __str__(self):
        return self.user.username

 

##Post

class Post(models.Model):
    title = models.CharField(max_length=100)
    model = models.FileField(blank=True, null=True, upload_to="models/%Y/%m/$D/",default="models/2022/04/$D/Earth.glb")
    # images = models.CharField(max_length=2000, default=None, blank=True, null=True )
    text_content = models.TextField(max_length=1000, default=None, blank=True, null=True)
    tags = models.TextField(max_length=1000, default=None, blank=True, null=True)
    downloads = models.IntegerField(default=0)
    type = models.CharField(max_length=50, default="STL")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def get_absolute_url(self):
        print("here")
        return reverse("post_detail", kwargs={"pk": self.id})
    
    def __str__(self):
        return self.title

    # comments = models.ManyToManyField(Account)
    # favorites = models.ManyToManyField(Account)


## Comment
class Comment(models.Model):
    #username = models.CharField(max_length=200, default=None, blank=True)
    images = models.CharField(max_length=2000, default=None, blank=True, null=True)
    text_content = models.CharField(max_length=3000)
    title = models.CharField(max_length=100)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE,blank=True, null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    # account = models.ForeignKey(Post, on_delete=models.CASCADE)
    # created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    
    # class Meta:
    #     ordering = ['created_on']
    def get_absolute_url(self):
        print('MM', self.post.id)
        return reverse("post_detail", kwargs={"pk": self.post.id})
    
    def __str__(self):
        return '{}'.format(self.title)
    
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    

