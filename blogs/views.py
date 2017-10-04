# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions, authentication
from django.utils import timezone

from models import Category, Post, Comment, Like
from serializers import CategorySerializer, PostSerializer, CategoryDetailSerializer, PostDetailSerializer, \
    CommentsSerializer, CommentDetailSerializer


def index(request):
    categories = Category.objects.all()
    serializier = CategorySerializer(categories, many=True)
    return JsonResponse(serializier.data, safe=False)


class CategoryListing(APIView):
    def get(self, request, format=None):
        snippets = Category.objects.all()
        serializer = CategorySerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            category = Category.objects.get(pk=pk)
            category_serializer = CategoryDetailSerializer(category)
            return Response(category_serializer.data)
        except Category.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

    def post(self, request, pk, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['created_by'] = request.user
            serializer.validated_data['category'] = Category.objects.get(pk=pk)
            serializer.validated_data['date_created'] = timezone.now()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
            post_serializer = PostDetailSerializer(post)
            return Response(post_serializer.data)
        except Post.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

    def post(self, request, pk, format=None):
        serializer = CommentsSerializer(data=request.data)
        post = Post.objects.get(pk=pk)
        date = timezone.now()
        user = request.user
        if serializer.is_valid():
            serializer.validated_data['post'] = post
            serializer.validated_data['user'] = user
            serializer.validated_data['dated'] = date
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
            if request.user == post.created_by:
                post.delete()
                return Response(status.HTTP_204_NO_CONTENT)
            else:
                return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
        except Post.DoesNotExist:
            return Response(status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
            if post.created_by == request.user:
                post_serializer = PostSerializer(post, data=request.data)
                if post_serializer.is_valid():
                    post_serializer.save()
                    return Response(post_serializer.data)
                else:
                    return Response(status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
        except Post.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)


class CommentDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            comment = Comment.objects.get(pk=pk)
            comment_serializer = CommentDetailSerializer(comment)
            return Response(comment_serializer.data)
        except Comment.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        try:
            comment = Comment.objects.get(pk=pk)
            if comment.user == request.user:
                comment_serializer = CommentDetailSerializer(comment)
                return Response(comment_serializer.data)
            else:
                return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
        except Comment.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        try:
            comment = Comment.objects.get(pk=pk)
            if request.data['type'] == 'update':
                if comment.user == request.user:
                    comment_serializer = CommentsSerializer(comment, data=request.data)
                    if comment_serializer.is_valid():
                        comment_serializer.save()
                        return Response(comment_serializer.data)
                    else:
                        return Response(status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
            elif request.data['type'] == 'like':
                already_liked_user = comment.get_users
                if request.user not in already_liked_user:
                    like = Like()
                    like.comment = comment
                    like.user = request.user
                    like.save()
                    return Response(status.HTTP_201_CREATED)
                else:
                    return Response(status.HTTP_501_NOT_IMPLEMENTED)
            elif request.data['type'] == 'unlike':
                already_liked_user = comment.get_users
                if request.user in already_liked_user:
                    like = Like.objects.get(user=request.user, comment=comment)
                    like.delete()
                    return Response(status.HTTP_201_CREATED)
            else:
                return Response(status.HTTP_501_NOT_IMPLEMENTED)
        except Comment.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
