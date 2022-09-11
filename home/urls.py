from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog', views.blog, name='blog'),
    path('blogpost/<str:post_slug>', views.blogpost, name='blogpost'),
    path('contact', views.contact, name='contact'),
    path('search', views.search, name='search'),
    path('blog/tagged/<str:tag>', views.tagged_posts, name='tagged_posts')
]
