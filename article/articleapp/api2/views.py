from rest_framework import generics, permissions
from articleapp.models import Article, Author, Comment, RoleAuthor
from articleapp.api2.serializer import (ArticleListSerializer,
                                       ArticleSerializer)
from articleapp.api.permissions import AuthorPermission

from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from rest_framework.exceptions import PermissionDenied
from django.db.models import Count



class ArticleList(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArticleListSerializer
    queryset = Article.objects.filter(deleted=False).prefetch_related('comments').annotate(comments_count=Count('comments')).order_by('-comments_count')

class ArticleDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [AuthorPermission, ]
    queryset = Article.objects.filter(deleted=False).prefetch_related('comments')
    serializer_class = ArticleSerializer 