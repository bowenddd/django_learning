from django.shortcuts import render, get_object_or_404
from .models import BlogArticles
from django.contrib.auth.decorators import login_required
from article.models import ArticlePost
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
# Create your views here.

@login_required()
def blog_titles(request):
    blog = ArticlePost.objects.filter(auth=request.user)
    paginator = Paginator(blog,3)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    blogs = current_page.object_list
    username = request.user.username
    return render(request, 'blog/titles.html', {'blogs':blogs,"username":username,"page":current_page})
@login_required()
def blog_content(request,article_id):
    blog = get_object_or_404(BlogArticles, id=article_id)
    publish = blog.publish
    return render(request, 'blog/content.html',{'blog':blog, 'publish':publish})