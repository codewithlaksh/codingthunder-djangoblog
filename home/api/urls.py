from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_api_routes, name='get_api_routes'),
    path('signup', views.user_signup, name='user_signup'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),
    path('postcomment', views.post_comment, name='post_comment'),
    path('contact', views.contact, name='contact')
]
