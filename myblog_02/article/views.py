from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from .forms import ArticleColumnForm,ArticlePostForm
from .models import ArticleColumn,ArticlePost
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

@login_required()
@csrf_exempt
def article_column(request):
    if request.method == 'GET':
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, 'article/column/article_column.html', {"columns":columns,"column_form":column_form})
    if request.method == 'POST':
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user=request.user, column=column_name)

        if columns:
            return HttpResponse("2")
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse("1")


@login_required()
@csrf_exempt
@require_POST
def edit_column(request):
    try:
        column_name = request.POST['column_name']
        column_id = request.POST['column_id']
        col = ArticleColumn.objects.get(id=column_id)
        col.column = column_name
        col.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

@login_required()
@csrf_exempt
@require_POST
def del_column(request):
    try:
        column_id = request.POST['column_id']
        col = ArticleColumn.objects.get(id=column_id)
        col.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

@login_required
@csrf_exempt
def article_post(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.auth = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column'])
                new_article.save()
                return HttpResponse("1")
            except Exception as e:
                print(e)
                return HttpResponse("0")
        else:
            return HttpResponse("2")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        return render(request,'article/column/article_post.html',{"article_post_form":article_post_form,"article_columns":article_columns})

@login_required
def article_list(request):
    article_list = ArticlePost.objects.filter(auth=request.user)
    paginator = Paginator(article_list,5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    # except EmptyPage:
    #     current_page = paginator.page(paginator.num_pages)
    articles = current_page.object_list
    return render(request,'article/column/article_list.html',{"articles":articles,"page":current_page})

@login_required
def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    return render(request,'article/column/article_detail.html',{'article':article})

@login_required
@csrf_exempt
@require_POST
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.filter(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

@login_required
@csrf_exempt
def edit_article(request,article_id):
    if request.method == 'GET':
        user = request.user
        article_columns = ArticleColumn.objects.filter(user=user)
        article = ArticlePost.objects.get(id=article_id)
        article_form = ArticlePostForm(initial={'title':article.title})
        article_column = article.column
        return render(request,'article/column/edit_article.html',{
            "article_columns" : article_columns,
            "article": article,
            "article_form" : article_form,
            "article_column" : article_column,
        })
    else:
        edit_article = ArticlePost(id=article_id)
        edit_article.title = request.POST['title']
        edit_article.body = request.POST['body']
        edit_article.column = request.user.article_column.get(id=request.POST['column'])
        edit_article.auth = request.user
        edit_article.save()
        return HttpResponse("1")