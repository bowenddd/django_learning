from django.shortcuts import render, get_object_or_404
from .models import BlogArticles
# Create your views here.

def show_title(request):
    blogs = BlogArticles.objects.all()
    return render(request, 'blog/title.html', {'blogs':blogs})

def show_content(request,article_id):
    blog = get_object_or_404(BlogArticles,id=article_id)
    publish = blog.publish
    return render(request, 'blog/content.html', {'blog':blog, 'publish':publish})