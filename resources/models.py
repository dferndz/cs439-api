from django.db import models
from uuid import uuid4


class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=1024, blank=True)
    image_src = models.TextField(blank=True)

    def __str__(self):
        return self.title
