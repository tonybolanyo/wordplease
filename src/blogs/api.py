from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from blogs.models import Post
from blogs.serializers import PostSerializer


class PostListAPIView(ListAPIView):

    serializer_class = PostSerializer

    def get_queryset(self):
        author = self.kwargs.get('author_name')
        queryset = Post.objects.filter(author__username=author)
        return queryset


class PostCreateAPIView(CreateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
