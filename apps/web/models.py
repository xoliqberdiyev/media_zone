from django.db import models

from apps.shared.models import BaseModel


class Partner(BaseModel):
    icon = models.FileField(upload_to='media_zone/partners')
    instagram_link = models.URLField(null=True, blank=True)

    def delete(self):
        self.icon.delete()
        return super().delete()


class Image(BaseModel):
    image = models.ImageField(upload_to='media_zone/images')

    def delete(self):
        self.image.delete()
        return super().delete()


class Video(BaseModel):
    video = models.FileField(upload_to="media_zone/videos")

    def delete(self):
        self.video.delete()
        return super().delete()


class Team(BaseModel):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="media_zone/teams")

    def delete(self):
        self.image.delete()
        return super().delete()
