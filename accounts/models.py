from django.db import models
from django.contrib.auth.models import User
from django.db import models
# from .import forms  

# Create your models here.
class signupModel(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    password2 = models.CharField(max_length=30)

class Authentication(models.Model):
    user = models.ForeignKey(User ,blank=True,default=True,on_delete=models.CASCADE, related_name="user")
    token = models.CharField(max_length=35, blank=True)

    def __str__(self):
        return self.user.username