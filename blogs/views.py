# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions, authentication
from django.utils import timezone

from models import Category
from serializers import CategorySerializer, PostSerializer


def index(request):
    categories = Category.objects.all()
    serializier = CategorySerializer(categories, many=True)
    return JsonResponse(serializier.data, safe=False)


class IndexView(APIView):
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

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


class PostIndexView(APIView):
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        category = Category.objects.get(pk=pk)
        posts = category.get_posts
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = PostSerializer(data=request.data)
        serializer.created_by = request.user
        serializer.category = Category.objects.get(pk=pk)
        serializer.date_created = timezone.now()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
