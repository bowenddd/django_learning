from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.blog_titles, name='blog_title'),
    path('<int:article_id>/', views.blog_content, name='blog_content')
]