from django.conf import settings
from django.db import models

from utils.models import TimeStampedModel


class Blog(TimeStampedModel):

    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '{title} by {author}'.format(title=self.title, author=self.author)
