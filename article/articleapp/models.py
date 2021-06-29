from django.db import models


from django.db import models
from django.contrib.auth.models import User



    

class RoleAuthor(models.Model):
    """ Role class for authors """

    name_role = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False, blank=True)
    deleted =  models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name_role




class Author(models.Model):
    """ Author class model """

    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='create_user', null=True)
    role =  models.ForeignKey(RoleAuthor, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=False, blank=True)
    deleted = models.BooleanField(default=False, blank=True)
    

    def __str__(self):
        return self.name



class Article(models.Model):
    """ Articles class model """

    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to = "images/")
    create_date =  models.DateTimeField(auto_now_add=True, null=True)
    update_date =  models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.BooleanField(default=False, blank=True)
    liked = models.ManyToManyField(Author, related_name='likes', default=None, blank=True)
    

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return self.title



class CommentManager(models.Manager):

    def all(self):
        queryset = super(CommentManager, self).filter(parent=None)
        return queryset


class Comment(models.Model):
    """ Comment class model """

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name='authors',default=None, blank=True, null=True)
    content = models.TextField(blank=True)
    create_date =  models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.BooleanField(default=False, blank=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, related_name='comments', null= True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,  null= True, blank=True)

    objects = CommentManager()
   
    def __str__(self):
        return self.content[:20] + "..."


    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True