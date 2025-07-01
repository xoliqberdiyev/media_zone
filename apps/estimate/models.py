from django.db import models

from apps.shared.models import BaseModel


class Estimate(BaseModel):
    TYPE = (
        ('INCOME', 'income'),
        ('EXPENCE', 'expence')
    )

    type = models.CharField(max_length=15, choices=TYPE)
    reason = models.CharField(max_length=250)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.reason