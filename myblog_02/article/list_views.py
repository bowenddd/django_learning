from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import ArticlePost, ArticleColumn

def article_titles(request):
    articles_title = ArticlePost.objects.all()
    paginator = Paginator(articles_title,3)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    articles = current_page.object_list
    return render(request,'article/list/article_titles.html',{
        "articles":articles,
        "page" : current_page
    })

def article_content(request,id,slug):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    return render(request,'article/list/article_content.html',{"article":article})