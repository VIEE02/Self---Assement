from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    mssv = models.CharField(max_length=255,blank=True, null=True)
    classname = models.CharField(max_length=255,blank=True, null=True)
    fullname = models.CharField(max_length=255,blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    password = models.CharField(max_length=128)
    following_user_id = models.CharField(max_length=512,blank=True, null=True)
    followed_user_id = models.CharField(max_length=512,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Group(models.Model):
    following_user_id = models.IntegerField(blank=True,null=True)
    followed_user_id = models.IntegerField(blank=True,null=True)
    groupname = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'group'


class DanhGia(models.Model):
    groupid = models.IntegerField()
    title = models.CharField(max_length=255)
    danhgia = models.TextField(verbose_name='Đánh giá')
    user_id = models.IntegerField()
    typedanhgia = models.IntegerField()
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    score3 = models.IntegerField()
    score = models.FloatField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nguoidanhgia = models.CharField(max_length=255)

    class Meta:
        db_table = 'danhgia'
