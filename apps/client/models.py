from django.db import models

from apps.shared.models import BaseModel

NEW, IN_PROGRESS, CANCELLED, DONE = ('new', 'in_progress', 'cancelled', 'done')

class Client(BaseModel):
    STATUS = (
        (NEW, 'new'),
        (IN_PROGRESS, 'in_progress'),
        (CANCELLED, 'cancelled'),
        (DONE, 'done')
    )

    name = models.CharField(max_length=50, db_index=True)
    phone = models.CharField(max_length=15, unique=True, db_index=True)
    status = models.CharField(max_length=12, choices=STATUS)

    def __str__(self):
        return f'{self.name} - {self.status}'
    

class ClientComment(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='comments')
    date = models.DateField()
    comment = models.TextField()

    def __str__(self):
        return self.comment

