import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 
        