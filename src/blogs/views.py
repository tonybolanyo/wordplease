from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, TemplateView, CreateView

from .models import Post


class HomePageView(ListView):

    model = Post
    template_name = 'home.html'

    def get_queryset(self):
        queryset = super(HomePageView, self).get_queryset()
        return queryset.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class BlogListView(TemplateView):

    pass


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'summary', 'body', 'categories', 'featured_media', 'pub_date')
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreatePostView, self).form_valid(form)


class PostsByAuthorView(ListView):

    model = Post
    template_name = 'blogs/posts_by_author.html'

    def get_queryset(self):
        queryset = super(PostsByAuthorView, self).get_queryset()
        author_name = self.kwargs['author_name']
        return queryset.filter(author__username=author_name, pub_date__lte=timezone.now()).order_by('-pub_date')
