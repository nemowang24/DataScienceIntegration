from django.contrib import admin
from .models import Article, Comment


# Register your models here.


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

class ArticleAdmin2(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = [
        "title",
        "body",
        "author",
        "date"
    ]


admin.site.register(Article, ArticleAdmin2)
admin.site.register(Comment)