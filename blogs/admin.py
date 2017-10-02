# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from blogs.models import Comment, Category, Like, Post

admin.site.register(Comment)
admin.site.register(Like)


class AdminCategoryModel(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)
    list_filter = ('name',)


class AdminPostModel(admin.ModelAdmin):
    list_display = ('title', 'category_name', 'username')
    list_filter = ['category__name', 'created_by']

    def category_name(self, obj):
        return obj.category.name

    def username(self, obj):
        return obj.created_by.username

    category_name.short_description = "Category"
    username.short_description = 'Posted By'


admin.site.register(Category, AdminCategoryModel)
admin.site.register(Post, AdminPostModel)
