import os
from django.conf import settings
from django.db import models
from django.utils import timezone

from utils.models import TimeStampedModel



class Category(TimeStampedModel, models.Model):

    name = models.CharField(max_length=30)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(TimeStampedModel, models.Model):

    def get_upload_path(instance, filename):
        username = instance.author.username
        today = timezone.now()
        return os.sep.join([username, 'featured', str(today.year), str(today.month), filename])

    title = models.CharField(max_length=100)
    summary = models.TextField()
    body = models.TextField()
    featured_media = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    pub_date = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    categories = models.ManyToManyField(Category)

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = '-pub_date'

    def __str__(self):
        return self.title
