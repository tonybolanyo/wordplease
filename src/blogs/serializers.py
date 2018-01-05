from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

from .models import Post


User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BlogSerializer(serializers.ModelSerializer):

    posts_count = serializers.IntegerField()
    last_post_date = serializers.DateTimeField()
    blog_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'posts_count', 'last_post_date', 'blog_url')

    def get_blog_url(self, instance):
        return reverse_lazy('api_posts_list', kwargs={'author_name': instance.username})


class PostBasicSerializer(serializers.ModelSerializer):

    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'featured_media', 'is_featured_video', 'summary', 'pub_date', 'author')


class PostSerializer(PostBasicSerializer):

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', 'author', 'created', 'updated')
