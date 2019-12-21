from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .models import ArticlePost, ArticleColumn, Comment
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
import redis
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse

db_redis = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)
def article_titles(request, username=None):
    user = None
    userinfo = None
    photo = None
    if username:
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(auth=user)
        try:
            userinfo = user.userinfo
            photo = userinfo.photo
            if(len(str(photo)) == 0):
                photo = None
        except:
            userinfo = None
    else:
        articles_title = ArticlePost.objects.all()
    paginator = Paginator(articles_title,3)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
    except EmptyPage:
        current_page = paginator.page(1)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    articles = current_page.object_list
    if username:
        return render(request,'article/list/author_articles.html',{
            "articles":articles,
            "page":current_page,
            "auth":user,
            "userinfo":userinfo,
            "photo":photo
        })
    else:
        return render(request,'article/list/article_titles.html',{
            "articles":articles,
            "page" : current_page
        })

def article_content(request,id,slug):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    views = db_redis.incr("article:{}:views".format(article.id))
    db_redis.zincrby("article_ranking",1,article.id)
    article_ranking = db_redis.zrange("article_ranking",0,-1,desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = [ArticlePost.objects.get(id=id) for id in article_ranking_ids]
    if request.method == 'POST':
        if(isinstance(request.user,AnonymousUser)):
            path = article.get_url_path()
            return HttpResponseRedirect(reverse("account:user_login")+"?next="+path)
        else:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.article = article
                new_comment.commentator = request.user
                new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,'article/list/article_content.html',
                  {"article":article,'views':views,
                   "most_viewed":most_viewed,"comment_form":comment_form})