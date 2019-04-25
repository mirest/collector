import uuid

from django.db import models


class BaseModel(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
