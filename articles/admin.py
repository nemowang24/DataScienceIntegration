from django.contrib import admin
from .models import Article


# Register your models here.

class ArticleAdmin3(admin.ModelAdmin):
    list_display2 = [
        "title",
        "body",
    ]


class ArticleAdmin2(admin.ModelAdmin):
    list_display2 = [
        "title",
        "body",
        "author",
        "date"
    ]




admin.site.register(Article, ArticleAdmin2)

