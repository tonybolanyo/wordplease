import os
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from utils.models import TimeStampedModel
from utils.validators import ContentTypeValidator, MaxFileSizeValidator


class Category(TimeStampedModel, models.Model):

    name = models.CharField(_('name'), max_length=30)

    class Meta:
        ordering = ['name']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


class Post(TimeStampedModel, models.Model):

    def get_upload_path(instance, filename):
        username = instance.author.username
        today = timezone.now()
        return os.sep.join([username, 'featured', str(today.year), str(today.month), filename])

    title = models.CharField(_('title'), max_length=100)
    summary = models.TextField(_('summary'))
    body = models.TextField(_('body'))
    featured_media = models.FileField(_('featured media'), upload_to=get_upload_path, null=True, blank=True,
                                      validators=[ContentTypeValidator(
                                          accepted_types=settings.ALLOWED_IMAGE_MIME_TYPES +
                                                         settings.ALLOWED_VIDEO_MIME_TYPES),
                                      MaxFileSizeValidator(max_size=settings.MAX_UPLOAD_SIZE)])
    is_featured_video = models.BooleanField(_('is featured video?'), default=False)
    pub_date = models.DateTimeField(_('publication date'), default=timezone.now)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('author')
    )

    categories = models.ManyToManyField(Category)

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = '-pub_date'
        verbose_name = _('post')

    def __str__(self):
        return self.title
