from rest_framework import serializers 
  
from rest_framework.serializers import  ModelSerializer
   
from articleapp.models import Article, Author, RoleAuthor, Comment
from rest_framework.response import Response
from django.contrib.auth.models import User




class CommentListSerializer(serializers.ModelSerializer):

    reply_count = serializers.SerializerMethodField()
    author = serializers.CharField(read_only=True)
    class Meta:
        model = Comment
        fields = ['id','author','content','create_date','article','parent','reply_count']

    def get_reply_count(self,obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
    


class CommentChildren(serializers.ModelSerializer):
    author = serializers.CharField()

    class Meta:
        model = Comment
        fields = ['id','content','author','create_date']


class CommentDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    replies = serializers.SerializerMethodField()
    parent = serializers.CharField(read_only=True)
    class Meta:
        model = Comment
        fields = ['id','author','content','create_date','replies','parent']

    def get_replies(self,obj):
        if obj.is_parent:
            return CommentChildren(obj.children(),many=True).data
        return None




class AuthorListSerializer(serializers.ModelSerializer):
    """ serializimi i listes autorve """

    class Meta:
        model = Author
        fields = ['name',]



#### Article Serializer ####
  

class ArticleListSerializer(serializers.ModelSerializer):
    """ serializimi i listes te artikujve  """

    total_liked = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    author = serializers.CharField(read_only=True)
    class Meta:
        model = Article 
        fields =  ['id', 'title','content','author','image','create_date','total_liked','total_comments',]
        read_only_fields = ['liked'] 
    

    def get_total_comments(self,obj):
        return obj.comments.all().count()

    def get_total_liked(self,obj):
        return obj.liked.all().count()

      

class ArticleSerializer(serializers.ModelSerializer):
    """serializimi krijmit dhe updateimi i artikullit"""

    liked = AuthorListSerializer(read_only=True, many = True)
    author = serializers.CharField(read_only=True)
    comments = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField(source='get_image')
    class Meta:
        model = Article
        fields =  ['id', 'title','content','author','image','create_date','liked','comments']

    @staticmethod
    def get_comments(obj):
        return CommentListSerializer(instance=obj.comments.filter(parent=None).order_by('-create_date'), many=True).data

    @staticmethod
    def get_image(obj):
        image_url = ""
        if obj.image:
            image_url = obj.image.url
        return image_url







    


    
