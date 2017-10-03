__author__ = 'waqarali'

from rest_framework import serializers

from models import Category, Post, Comment
from django.utils import timezone


class PostSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    Owner = serializers.ReadOnlyField(source='created_by.username')
    date_created = serializers.ReadOnlyField()
    is_deleted = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'category_name', 'Owner', 'date_created', 'is_deleted')

    def create(self, validated_data):
        validated_data['is_deleted'] = False
        validated_data['date_created'] = timezone.now()
        validated_data['category'] = self.category
        validated_data['created_by'] = self.created_by
        return self.Meta.model.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class CategoryDetailSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'posts')


class CommentsSerializer(serializers.ModelSerializer):
    commented_by = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ('text', 'dated', 'commented_by')


class PostDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    category_id = serializers.ReadOnlyField(source='category.id')
    created_by = serializers.ReadOnlyField(source='created_by.username')
    date_created = serializers.ReadOnlyField()
    comments = CommentsSerializer(many=True)

    class Meta:
        model = Post
        fields = ('title', 'category_name', 'category_id', 'created_by', 'date_created', 'comments')


