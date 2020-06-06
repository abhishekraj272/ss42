from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    dev_name = models.CharField(max_length=80, null=False)
    company_name = models.CharField(max_length=80, null=True)
    email = models.EmailField(null=False)
    city = models.CharField(max_length=100, null=False)
    country = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=1024, null=False)
    api_key = models.TextField(max_length=1024, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.dev_name
