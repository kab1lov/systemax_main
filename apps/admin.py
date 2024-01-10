from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.models import BlogInnerTextModel, BlogModel


@admin.register(BlogInnerTextModel)
class BlogInnerTextAdmin(ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)


@admin.register(BlogModel)
class BlogInnerTextAdmin(ModelAdmin):
    list_display = ('id', 'title', 'image', 'text')
    list_display_links = ('id', 'title',)
