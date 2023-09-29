import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from datetime import datetime as dt
from django.utils import timezone
from django.dispatch import receiver
from .user_manager import UserManager


class User(AbstractBaseUser):
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=50, unique=True)
    password = models.TextField()
    date_of_birth = models.DateField()
    contact_number = models.BigIntegerField()

    is_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table="User"
        
    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password', 'date_of_birth', 'contact_number']

class Chat(models.Model):
    sender_id = models.IntegerField()
    Receiver_id = models.IntegerField()
    msg = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Chat"
