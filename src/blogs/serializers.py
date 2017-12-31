from rest_framework import serializers

from .models import Post


class PostBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'featured_media', 'is_featured_video', 'summary', 'pub_date')


class PostSerializer(PostBasicSerializer):

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', 'author', 'created', 'updated')
