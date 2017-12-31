from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .permissions import IsOwnerAdminOrReadOnly
from .serializers import PostSerializer, PostBasicSerializer


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
