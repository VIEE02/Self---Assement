from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    following_user_id = models.IntegerField(null=True, blank=True)
    followed_user_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username
    

class User(models.Model):
    id = models.AutoField(primary_key=True)
    following_user_id = models.IntegerField()
    followed_user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Group(models.Model):
    following_user_id = models.IntegerField()
    followed_user_id = models.IntegerField()
    groupid = models.AutoField(primary_key=True)
    groupname = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class DanhGia(models.Model):
    id = models.AutoField(primary_key=True)
    groupid = models.IntegerField()
    title = models.CharField(max_length=255)
    danhgia = models.TextField(verbose_name='Đánh giá')
    user_id = models.IntegerField()
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
