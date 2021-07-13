from rest_framework import generics, permissions
from articleapp.models import Article, Author, Comment, RoleAuthor
from articleapp.api.serializer import (ArticleListSerializer,
                                       CommentDetailSerializer,CommentListSerializer,ArticleSerializer,)
from articleapp.api.permissions import AuthorPermission

from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin 
from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.db.models import Count



# class HPaginator(PageNumberPagination):
#     page_size = 10
    


class LikeArticle(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    article_lookup = 'pk'
    queryset = Article.objects.filter(deleted=False).prefetch_related('liked')

    @staticmethod
    def serialize_instance(instance: Article):
        serialzier = ArticleSerializer(instance=instance)
        return serialzier.data

    def get_article(self):
        article_id = self.kwargs.get(self.article_lookup, None)
        return get_object_or_404(self.queryset, id=article_id) 

    def get_author(self):
        return self.request.user.create_user

    def get(self, request, *args, **kwargs):
        article = self.get_article() 
        if liked := article.liked.filter(user__create_user=request.user.create_user.first()):
            article.liked.remove(self.get_author().first())
        else:
            article.liked.add(self.get_author().first())
            
        return Response(self.serialize_instance(article))


# class UnLikeArticle(APIView):
#     permission_classes = [permissions.IsAuthenticated, ]
#     article_lookup = 'pk'
#     queryset = Article.objects.filter(deleted=False).prefetch_related('liked')

#     @staticmethod
#     def serialize_instance(instance: Article):
#         serialzier = ArticleListSerializer(instance=instance)
#         return serialzier.data

#     def get_article(self):
#         article_id = self.kwargs.get(self.article_lookup, None)
#         return get_object_or_404(self.queryset, id=article_id) 

#     def get_author(self):
#         return self.request.user.create_user

#     def get(self, request, *args, **kwargs):
#         article = self.get_article()
#         article.liked.remove(self.get_author().first())
#         return Response(self.serialize_instance(article))


####  Article Views  ####


class  ArticleListAPIView(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArticleListSerializer
    #queryset = Article.objects.filter(deleted=False).prefetch_related('comments')
    paginator_class = PageNumberPagination

    def get_queryset(self):
        
        queryset = Article.objects.filter(deleted=False).prefetch_related('comments')
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__istartswith=title)
        queryset = queryset.order_by('-create_date')
        return queryset

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)

class ArticleDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AuthorPermission, ]
    queryset = Article.objects.filter(deleted=False).prefetch_related('comments')
    serializer_class = ArticleSerializer


####  Comment Views  ####


class  CommentListAPIView(ListCreateAPIView):
    permission_classes =  (permissions.IsAuthenticated,)
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()
    paginator_class = PageNumberPagination
	
    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)


class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    """ detajet , fshirja e komentit """
    queryset = Comment.objects.filter(deleted=False)
    serializer_class = CommentDetailSerializer
    permission_classes = [AuthorPermission, ]
  

