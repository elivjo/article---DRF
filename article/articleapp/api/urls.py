from django.urls import include,path
from articleapp.api.views import ( ArticleDetailAPIView,
                        CommentListAPIView,CommentDetailAPIView,ArticleListAPIView, LikeArticle, UnLikeArticle )
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
            path("", include(router.urls)),
            #path('login/', LoginAPIView.as_view(),name= "login"),
            path('articles/', ArticleListAPIView.as_view(), name= "article-list"),
            path('articles/<int:pk>/', ArticleDetailAPIView.as_view(), name= "article-detail"),
            path('articles/like/<int:pk>/', LikeArticle.as_view(), name='article-like'),
            path('articles/unlike/<int:pk>/', UnLikeArticle.as_view(), name='article-like'),
            path('comments/', CommentListAPIView.as_view(), name= "article-detail"),
            path('articles/<int:article_pk>/comments/<int:pk>/', CommentDetailAPIView.as_view(), name= "article-detail"),
            path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name= "article-detail"),
            
]