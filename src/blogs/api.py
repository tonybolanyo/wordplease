from django.utils import timezone
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from blogs.models import Post
from blogs.serializers import PostSerializer, PostBasicSerializer


class PostListAPIView(ListAPIView):

    serializer_class = PostBasicSerializer

    def get_queryset(self):
        author = self.kwargs.get('author_name')
        queryset = Post.objects.filter(author__username=author)
        user = self.request.user
        if user.username != author and not user.is_superuser:
            queryset = queryset.filter(pub_date__lte=timezone.now())
        return queryset


class PostCreateAPIView(CreateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
