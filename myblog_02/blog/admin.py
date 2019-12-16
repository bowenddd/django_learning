from django.contrib import admin
from .models import BlogArticles
# Register your models here.

class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish')
    list_filter = ('title', 'author')
    search_fields = ('title',)
    raw_id_fields = ("author",)
    date_hierarchy = "publish"

admin.site.register(BlogArticles, BlogArticlesAdmin)
