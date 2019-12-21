from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from slugify import slugify
from django.urls import reverse
# Create your models here.

class ArticleColumn(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='article_column')
    column = models.CharField(max_length=200)
    create = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticleTag(models.Model):
    auth = models.ForeignKey(User,on_delete=models.CASCADE,related_name="tag")

    tag = models.CharField(max_length=100)

class ArticlePost(models.Model):
    auth = models.ForeignKey(User,on_delete=models.CASCADE,related_name='article')
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=500)
    column = models.ForeignKey(ArticleColumn,on_delete=models.CASCADE,related_name='column_article')

    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    article_tag = models.ManyToManyField(ArticleTag,related_name='article_tag',blank=True)

    users_like = models.ManyToManyField(User,related_name='article_like',blank=True)
    class Meta:
        ordering = ('title',)
        index_together = (('id','slug'),)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        super(ArticlePost,self).save(force_insert,force_update,using,update_fields)

    def get_absolute_url(self):
        return reverse("article:article_detail",args=[self.id,self.slug])

    def get_url_path(self):
        return reverse("article:article_content",args=[self.id,self.slug])


class Comment(models.Model):
    article = models.ForeignKey(ArticlePost,on_delete=models.CASCADE,related_name='comments')

    commentator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='commentator')

    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "comment by {} on {}".format(self.commentator.username,self.article)

