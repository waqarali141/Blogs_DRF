__author__ = 'waqarali'

from rest_framework import serializers

from models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    Owner = serializers.ReadOnlyField(source='created_by.username')
    date_created = serializers.ReadOnlyField()
    is_deleted = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'category_name', 'Owner', 'date_created', 'is_deleted')
