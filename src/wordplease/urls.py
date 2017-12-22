"""wordplease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from blogs.views import HomePageView, BlogListView, CreatePostView, PostsByAuthorView
from users.views import LoginView, LogoutView, SignupView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blogs/<str:author_name>/', PostsByAuthorView.as_view(), name='posts_by_author'),
    path('new-post/', CreatePostView.as_view(), name='create_post'),
    path('login/', LoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(), name='logout_page'),
    path('signup/', SignupView.as_view(), name='signup_page'),
    path('', HomePageView.as_view(), name='home_page'),
]

if settings.DEBUG:
    urlpatterns += urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)