from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Post


User = get_user_model()


class BlogSerializer(serializers.ModelSerializer):

    posts_count = serializers.IntegerField()
    last_post_date = serializers.DateTimeField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'posts_count', 'last_post_date')


class PostBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'featured_media', 'is_featured_video', 'summary', 'pub_date')


class PostSerializer(PostBasicSerializer):

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', 'author', 'created', 'updated')
