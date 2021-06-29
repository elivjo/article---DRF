from rest_framework import permissions
from articleapp.models import Article


class AuthorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj: Article):
        if obj.author.user_id == request.user.id:
            return True
        elif request.method in permissions.SAFE_METHODS: 
            return True
        return False
