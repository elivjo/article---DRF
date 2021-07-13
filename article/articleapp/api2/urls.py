from django.urls import include,path
from articleapp.api2.views import ( ArticleDetail,
                      ArticleList, )
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
            path("", include(router.urls)),
            #path('login/', LoginAPIView.as_view(),name= "login"),
            path('artikull/', ArticleList.as_view(), name= "article-list"),
            path('artikull/<int:pk>/', ArticleDetail.as_view(), name= "article-detail"),
            
]