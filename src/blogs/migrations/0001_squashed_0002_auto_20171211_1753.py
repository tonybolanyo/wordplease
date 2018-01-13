# Generated by Django 2.0 on 2018-01-09 16:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils.models.time_stamped_model


class Migration(migrations.Migration):

    replaces = [('blogs', '0001_initial'), ('blogs', '0002_auto_20171211_1753')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('summary', models.TextField()),
                ('body', models.TextField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('created', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'get_latest_by': '-pub_date',
                'ordering': ['-pub_date'],
            },
            bases=(utils.models.time_stamped_model.TimeStampedModel, models.Model),
        ),
    ]