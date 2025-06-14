from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.shared.models import BaseModel


class User(BaseModel, AbstractUser):
    pass 
