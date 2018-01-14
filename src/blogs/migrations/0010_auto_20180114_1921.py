# Generated by Django 2.0 on 2018-01-14 18:21

import blogs.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0009_auto_20180114_1915'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'categoría', 'verbose_name_plural': 'categorías'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'get_latest_by': '-pub_date', 'ordering': ['-pub_date'], 'verbose_name': 'artículo'},
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='autor'),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(verbose_name='cuerpo'),
        ),
        migrations.AlterField(
            model_name='post',
            name='featured_media',
            field=models.FileField(blank=True, null=True, upload_to=blogs.models.Post.get_upload_path, validators=[utils.validators.ContentTypeValidator(accepted_types=['image/jpeg', 'image/png', 'image/gif', 'video/mpeg', 'video/quicktime', 'video/mp4']), utils.validators.MaxFileSizeValidator(max_size=1048576)], verbose_name='imagen o vídeo destacado'),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_featured_video',
            field=models.BooleanField(default=False, verbose_name='¿es un vídeo destacado?'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='fecha de publicación'),
        ),
        migrations.AlterField(
            model_name='post',
            name='summary',
            field=models.TextField(verbose_name='introducción'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100, verbose_name='título'),
        ),
    ]