from django.contrib import admin


# Register your models here.
from .models import Article, Author, RoleAuthor, Comment



admin.site.register(Article)
admin.site.register(Author)
admin.site.register(RoleAuthor)
admin.site.register(Comment)