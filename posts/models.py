from django.db import models
import uuid # new

from django.db import models # new
from django.shortcuts import reverse # new
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

User = get_user_model()
class PostAdvertisment(models.Model):
    # post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    # post=models.ForeignKey('Post',on_delete=models.CASCADE,related_name="postad",null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=255,null=True,blank=True)
    url=models.URLField(null=True,blank=True)
    advertizing_content= models.TextField(null =True ,blank=True)
    def __str__(self):
        return f'{self.title}'
class Post(models.Model):

    # created_at=models.DateTimeField(efault=datetime.now, blank=True)

    created_at=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="post")
    title=models.CharField(max_length=128,null=True,blank=True)
    rate=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)],default=True,null=True,blank=True)

    # rating=models.IntegerField(null=True,blank=True)
    content=models.TextField(null=True,blank=True)
    review=models.CharField(max_length=250,null=True,blank=True)
    url=models.URLField(null=True,blank=True)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="post_voters")
    tags = TaggableManager(blank=False)
    comments=models.ManyToManyField('Comment',blank=True,related_name="comments_post")
    anonymous = models.BooleanField(default=False, blank=True)
    fake = models.BooleanField(default=False, blank=True)

    genuine = models.ManyToManyField(settings.AUTH_USER_MODEL , blank=True, related_name="post_genuines")
    spam = models.ManyToManyField(settings.AUTH_USER_MODEL , blank=True, related_name="post_spames")
    advertisement=models.ForeignKey(PostAdvertisment,on_delete=models.CASCADE,null=True,blank=True,related_name="postadvertisement")




    def __str__(self):
        return f'{self.content}'
    def get_absolute_url(self):
        return reverse('post:post_detail' , kwargs={'post_id':Post.id})

class Message(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="msg")
    title=models.CharField(max_length=128,null=True,blank=True)
    # picture=models.ImageField(upload_to='fake_picture',max_length=255,null=True,blank=True)
    rate=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)],default=True,null=True,blank=True)
    genuine = models.ManyToManyField(settings.AUTH_USER_MODEL , blank=True, related_name="msg_genuines")
    spam = models.ManyToManyField(settings.AUTH_USER_MODEL , blank=True, related_name="msg_spames")
    # rating=models.IntegerField(null=True,blank=True)
    content=models.TextField(null=True,blank=True)
    review=models.CharField(max_length=250,null=True,blank=True)
    tags = TaggableManager(blank=True)
    fake = models.BooleanField(default=False, blank=True)
    anonymous = models.BooleanField(default=False, blank=True)
    # url=models.URLField(null=True,blank=True)
    # voters = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="post_voters")
    # tags = TaggableManager(blank=True)

    def __str__(self):
        return f'{self.content}'
    def get_absolute_url(self):
        return reverse('post:post_detail' , kwargs={'post_id':Post.id})
class Img(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="img")
    picture=models.ImageField(upload_to='fake_picture',null=True,blank=True)
    tags = TaggableManager(blank=True)
    genuine = models.ManyToManyField(settings.AUTH_USER_MODEL , blank=True, related_name="img_genuines")
    spam = models.ManyToManyField(settings.AUTH_USER_MODEL , blank=True, related_name="img_spames")
    fake = models.BooleanField(default=False, blank=True)
    anonymous = models.BooleanField(default=False, blank=True)

    # def no_of_rating(self):

    #     ratings=Rating.objects.filter(Post=self)
    #     return len(ratings)
    # def avg_rating(self):
    #     sum = 0
    #     ratings = Rating.objects.filter(Post=self)
    #     for rating in ratings:
    #         sum += rating.stars
    #
    #     if len(ratings) > 0:
    #         return sum / len(ratings)
    #     else:
    #         return 0

# class Rating(models.Model):
#     Post=models.ForeignKey(Post,on_delete=models.CASCADE)
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     stars=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
#     class Meta:
#         unique_together =(( 'user' ,'Post'),)
#         index_together =(( 'user' ,'Post'),)

class Comment(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    content=models.CharField(max_length=128,default=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_comments",default=True)
    author=models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,default=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.content
