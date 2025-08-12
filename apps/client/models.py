from django.db import models
from django.utils import timezone
from datetime import timedelta
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

    @property
    def back_color(self):
        latest_comment = self.comments.order_by('-date').first()
        if not latest_comment:
            return None  # oldin green edi

        today = timezone.now().date()
        comment_date = latest_comment.date
        days_diff = (comment_date - today).days

        if 1 <= days_diff <= 2:
            return 'yellow'
        elif days_diff < 1:
            return 'red'

        return None

class ClientComment(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='comments')
    date = models.DateField()
    comment = models.TextField()

    def __str__(self):
        return self.comment