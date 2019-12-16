from django.shortcuts import render, get_object_or_404
from .models import BlogArticles
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required()
def blog_titles(request):
    blogs = BlogArticles.objects.all()
    return render(request, 'blog/titles.html', {'blogs':blogs})
@login_required()
def blog_content(request,article_id):
    blog = get_object_or_404(BlogArticles, id=article_id)
    publish = blog.publish
    return render(request, 'blog/content.html',{'blog':blog, 'publish':publish})