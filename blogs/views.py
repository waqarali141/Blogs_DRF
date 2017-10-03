# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions, authentication
from django.utils import timezone

from models import Category, Post, Comment
from serializers import CategorySerializer, PostSerializer, CategoryDetailSerializer, PostDetailSerializer


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


class PostsListing(APIView):
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        category = Category.objects.get(pk=pk)
        category_serializer = CategoryDetailSerializer(category)
        return Response(category_serializer.data)

    def post(self, request, pk, format=None):
        serializer = PostSerializer(data=request.data)
        serializer.created_by = request.user
        serializer.category = Category.objects.get(pk=pk)
        serializer.date_created = timezone.now()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk , format=None):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListing(APIView):

    def get(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        post_serializer = PostDetailSerializer(post)
        return Response(post_serializer.data)