from django.contrib import admin
from .models import BlogArticles
# Register your models here.

class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish")
    list_filter = ("author", "publish")
    search_fields = ("author", "title")
    raw_id_fields = ("author",)
    date_hierarchy = "publish"

admin.site.register(BlogArticles, BlogArticlesAdmin)