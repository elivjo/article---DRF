from rest_framework import serializers 
  
from rest_framework.serializers import  ModelSerializer
   
from articleapp.models import Article, Author, RoleAuthor, Comment
from rest_framework.response import Response
from django.contrib.auth.models import User





class CommentListSerializer(serializers.ModelSerializer):
    
    reply_count = serializers.SerializerMethodField()

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
    #author = serializers.CharField()
    replies = serializers.SerializerMethodField()

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

    liked = AuthorListSerializer(read_only=True, many = True)
    comment = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()

    class Meta:
        model = Article 
        fields =  ['id', 'title','content','author','image','create_date','liked','total_comments','comment',]
        read_only_fields = ['liked']
    
    @staticmethod
    def get_comment(obj):
        return CommentListSerializer(instance=obj.comments.filter(parent=None), many=True).data[:1]

    def get_total_comments(self,obj):
        return obj.comments.all().count()

      

class ArticleSerializer(serializers.ModelSerializer):
    """serializimi krijmit dhe updateimi i artikullit"""

    author = serializers.CharField()
    comments = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField(source='get_image')
    class Meta:
        model = Article
        fields =  ['id', 'title','content','author','image','create_date','liked','comments']

    @staticmethod
    def get_comments(obj):
        return CommentListSerializer(instance=obj.comments.filter(parent=None), many=True).data

    @staticmethod
    def get_image(obj):
        image_url = ""
        if obj.image:
            image_url = obj.image.url
        return image_url








    


    
