import uuid
from datetime import datetime

from django.db import models
from django.db.models.query import QuerySet


class SoftDeletionManager(models.Manager):

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(is_deleted=False)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(is_deleted=True)

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()


class BaseModel(models.Model):
    identifier = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeletionManager()

    class Meta:
        abstract = True
        ordering = ['date_created']

    def delete(self):
        self.deleted_at = datetime.now()
        self.is_deleted = True
        self._soft_delete_cascade()
        self.save()

    def hard_delete(self):
        super(BaseModel, self).delete()

    def _soft_delete_cascade(self):
        related_objects = self._meta.related_objects
        for obj in related_objects:
            self.__getattribute__(obj.name).update(is_deleted=True)
