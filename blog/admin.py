from django.contrib import admin
from .models import Category, Article, Profile, Comment

# Register your models here.

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Profile)
admin.site.register(Comment)