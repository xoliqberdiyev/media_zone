from django.db import models

from apps.shared.models import BaseModel


class Partner(BaseModel):
    icon = models.ImageField(upload_to='partners')

class Image(BaseModel):
    image = models.ImageField(upload_to='images')


