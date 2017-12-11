from django.db import models

from utils.models import TimeStampedModel


class Category(TimeStampedModel, models.Model):
    """
    Allows sort blog posts. Every post must have at least one category
    but it can have several ones.

    Categories are editable from the admin site and all
    blogs share the same categories collection.
    """

    name = models.CharField(max_length=30)

    class Meta:
        ordering = ['name']
