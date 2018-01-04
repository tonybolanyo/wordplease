from django.contrib.auth import get_user_model
from django.db.models import Count, Max
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .permissions import IsOwnerAdminOrReadOnly
from .serializers import PostSerializer, PostBasicSerializer, BlogSerializer


User = get_user_model()


class OwnerAdminFuturePostMixin:

    def get_queryset(self):
        author = self.kwargs.get('author_name')
        queryset = Post.objects.filter(author__username=author)
        user = self.request.user
        if user.username != author and not user.is_superuser:
            queryset = queryset.filter(pub_date__lte=timezone.now())
        return queryset


class PostListAPIView(OwnerAdminFuturePostMixin, ListAPIView):

    serializer_class = PostBasicSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ('title', 'summary', 'body')
    filter_fields = ('categories',)
    ordering_fields = ('title', 'pub_date')
    # Esto no es realmente necesario ya que lo hemos especificado
    # en la clase `Meta` del modelo, pero así, independizamos el
    # comportamiento de la API del de la web y el administrador
    ordering = ('-pub_date',)

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


class PostDetailAPIView(OwnerAdminFuturePostMixin, RetrieveUpdateDestroyAPIView):

    serializer_class = PostSerializer
    permission_classes = [IsOwnerAdminOrReadOnly]


class BlogListAPIView(ListAPIView):

    """
    Solamente tiene en cuenta posts que no tengan fecha de
    publicación en el futuro.
    """

    serializer_class = BlogSerializer
    queryset = User.objects.filter(post__pub_date__lte=timezone.now()).annotate(
        posts_count=Count('post'), last_post_date=Max('post__pub_date')).filter(posts_count__gt=0)
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ('username', 'posts_count', 'last_post_date')
    ordering = '-last_post_date'
    search_fields = ('username',)
