from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, TemplateView, CreateView, DetailView

from .models import Post


User = get_user_model()


class HomePageView(ListView):

    model = Post
    template_name = 'home.html'
    paginate_by = settings.PAGINATION_DEFAULT_SIZE

    def get_queryset(self):
        queryset = super(HomePageView, self).get_queryset()
        return queryset.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class BlogListView(ListView):

    template_name = 'blogs/blog_list.html'
    paginate_by = settings.PAGINATION_DEFAULT_SIZE

    def get_queryset(self):
        queryset = Post.objects.filter(
            pub_date__lte=timezone.now()).values(
            'author__username', 'author__first_name', 'author__last_name').annotate(
            num_posts=Count('id'), last_post=Max('pub_date')).order_by('author__username')
        return queryset


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'summary', 'body', 'categories', 'featured_media', 'pub_date')
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        form.instance.author = self.request.user
        mime_type = form.instance.featured_media.file.content_type
        # Como ya está validado, o es un vídeo o una imagen de los tipos aceptados
        # así que basta con comprobar si es un vídeo.
        form.instance.is_featured_video = mime_type in settings.ALLOWED_VIDEO_MIME_TYPES
        return super(CreatePostView, self).form_valid(form)


class PostsByAuthorView(ListView):

    model = Post
    template_name = 'blogs/posts_by_author.html'
    paginate_by = settings.PAGINATION_DEFAULT_SIZE

    def get_queryset(self):
        queryset = super(PostsByAuthorView, self).get_queryset()
        author_name = self.kwargs.get('author_name')
        return queryset.filter(author__username=author_name, pub_date__lte=timezone.now()).order_by('-pub_date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        author_name = self.kwargs.get('author_name')
        user = get_object_or_404(User, username=author_name)
        context['author'] = user
        return context


class PostDetailView(DetailView):

    model = Post

    def get_queryset(self):
        author = self.kwargs.get('author_name')
        pk = self.kwargs.get('pk')
        queryset = Post.objects.filter(author__username=author, pk=pk)
        return queryset
