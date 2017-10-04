__author__ = 'waqarali'

from rest_framework import serializers

from models import Category, Post, Comment, Like


class PostSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    Owner = serializers.ReadOnlyField(source='created_by.username')
    date_created = serializers.ReadOnlyField()
    is_deleted = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'category_name', 'Owner', 'date_created', 'is_deleted')


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
    dated = serializers.ReadOnlyField()
    comment = serializers.CharField(source='text')

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'dated', 'commented_by')


class PostDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    category_id = serializers.ReadOnlyField(source='category.id')
    created_by = serializers.ReadOnlyField(source='created_by.username')
    date_created = serializers.ReadOnlyField()
    comments = CommentsSerializer(many=True)

    class Meta:
        model = Post
        fields = ('title', 'category_name', 'category_id', 'created_by', 'date_created', 'comments')


class LikeSerializer(serializers.ModelSerializer):
    User = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ('User',)


class CommentDetailSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(source='text')
    Date = serializers.DateTimeField(source='dated')
    is_deleted = serializers.ReadOnlyField()
    likes = LikeSerializer(many=True)
    like_count = serializers.SerializerMethodField()
    commented_by = serializers.CharField(source='user.username')

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'Date', 'is_deleted', 'likes', 'like_count', 'commented_by')

    def get_like_count(self, obj):
        return obj.likes.count()
