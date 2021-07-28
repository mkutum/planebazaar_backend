from rest_framework import permissions
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission

from .models import Users, Blacklisted
from rest_framework.exceptions import AuthenticationFailed

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.GET.get('user_name')
        if username is None:
            return None
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            raise AuthenticationFailed('No Such User')
        return (user, None)

    def has_permission(self, request, view):
        return request.user.is_staff


class IsAdminOrStaff(BasePermission):
    message = 'None of permissions requirements fulfilled.'

    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_staff


class IsOwner(BasePermission):
    """
      Custom permission to only allow owners of an object to edit it.
      """
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        else:
            return False

    """ def has_permission(self, request, view):
            return request.user and request.user.is_authenticated()
    
        def has_object_permission(self, request, view, obj):
            return obj.user == request.user
        """


class BlocklistUserPermission(BasePermission):
    """
    Global permission check for blocked Org.
    """

    def has_permission(self, request, view, obj):
        org_id = request.META['Org_id']  # has to check
        blocked = Blacklisted.objects.filter(org_id=org_id).exists()
        return not blocked