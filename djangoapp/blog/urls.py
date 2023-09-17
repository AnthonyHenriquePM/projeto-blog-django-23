from django.urls import path
from blog.views import index, post, page

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('post/', post, name='index'),
    path('page/', page, name='index'),
]
