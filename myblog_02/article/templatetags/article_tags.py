from django import template

from article.models import ArticlePost
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def total_articies():
    return ArticlePost.objects.count()

@register.simple_tag
def author_total_articles(user):
    return user.article.count()

@register.inclusion_tag("article/list/latest_articles.html")
def latest_articles(n=5):
    articles = ArticlePost.objects.order_by('-created')[:n]
    return {"latest_articles":articles}

@register.simple_tag
def most_commented_articles(n=3):
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by("-total_comments")[:n]

@register.filter(name='markdown')
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))

@register.simple_tag
def similar_articles(this_article):
    this_article_tags_ids = this_article.article_tag.values_list("id",flat=True)
    articles = ArticlePost.objects.all()
    same_tags = []
    similar_ids = []
    for article in articles:
        if article.id == this_article.id:
            continue
        article_tags_ids = article.article_tag.values_list("id",flat=True)
        count = 0
        for tag_id in article_tags_ids:
            if tag_id in this_article_tags_ids:
                count += 1
        if(count!=0):
            similar_ids.append(article.id)
            same_tags.append(count)
    s = similar_ids.copy()
    similar_ids.sort(key=lambda x:same_tags[s.index(x)],reverse=True)
    similar_articles = [ArticlePost.objects.get(id=a_id) for a_id in similar_ids]
    return similar_articles
