from django.utils import timezone
from django.views.generic import ListView

from blogs.models import Post
from blogs.models.blog import Blog


class HomePageView(ListView):

    model = Post
    template_name = 'home.html'

    def get_queryset(self):
        queryset = super(HomePageView, self).get_queryset()
        return queryset.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class BlogListView(ListView):

    model = Blog