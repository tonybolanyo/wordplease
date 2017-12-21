from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, TemplateView, CreateView

from blogs.models import Post


class HomePageView(ListView):

    model = Post
    template_name = 'home.html'

    def get_queryset(self):
        queryset = super(HomePageView, self).get_queryset()
        return queryset.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class BlogListView(TemplateView):
    pass


class CreatePostView(CreateView):
    model = Post
    fields = '__all__'
    success_url = reverse_lazy('home_page')