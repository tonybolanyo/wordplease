from django.conf import settings
from django.db import models
from django.utils import timezone

from blogs.models.blog import Blog
from utils.models import TimeStampedModel


class Post(TimeStampedModel, models.Model):

    title = models.CharField(max_length=100)
    summary = models.TextField()
    body = models.TextField()
    # featured_media = models.ImageFile()
    pub_date = models.DateTimeField(default=timezone.now)

    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = '-pub_date'

    def __str__(self):
        return self.title
