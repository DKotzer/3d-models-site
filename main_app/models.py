from audioop import reverse
from django.db import models
from django.forms import ImageField
from pkg_resources import to_filename
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.shortcuts import redirect, render

class Account(models.Model):

    picture = models.FileField(blank=True, null=True, upload_to="models/accountImg", default="/media/models/accountImg/default.png" )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('profile', kwargs = {'account_id': self.id})
    
    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=100)
    model = models.FileField(blank=True, null=True, upload_to="models/%Y/%m/$D/",default="/media/models/Earth.glb")
    text_content = models.TextField(max_length=500, default=None, blank=True, null=True)
    tags = models.TextField(max_length=1000, default=None, blank=True, null=True)
    downloads = models.IntegerField(default=0)
    type = models.CharField(max_length=50, default="GLB")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes')
    
    def total_likes(self):
        return self.likes.count()
    
    def get_absolute_url(self):
        print("here")
        return reverse("post_detail", kwargs={"pk": self.id})
    
    def __str__(self):
        return self.title


class Comment(models.Model):
   
    text_content = models.CharField(max_length=3000)
    title = models.CharField(max_length=100)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        print('MM', self.post.id)
        return reverse("post_detail", kwargs={"pk": self.post.id})
    
    def __str__(self):
        return '{}'.format(self.title)
    
class Photo(models.Model):
    url = models.CharField(max_length=3000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    

    

