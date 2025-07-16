from django.db import models

from apps.shared.models import BaseModel


class Partner(BaseModel):
    icon = models.FileField(upload_to='partners')

class Image(BaseModel):
    image = models.ImageField(upload_to='images')

class Video(BaseModel):
    video = models.FileField(upload_to="videos")


class Team(BaseModel):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="teams")

