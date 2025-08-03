from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.shared.models import BaseModel


class User(BaseModel, AbstractUser):
    role = models.CharField(choices=[('admin', 'admin',), ('operator', 'operator')], max_length=20, default='operator')