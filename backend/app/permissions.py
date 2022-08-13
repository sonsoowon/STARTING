from rest_framework import permissions
from .models import *

# Object 단위 허용 권한
# Manager > allow retrieve(GET), create(POST), update(PUT), delete(DELETE)
# Not Manager > allow only retrieve(GET)
class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Permission for POST, PUT, DELETE to only allow managers of a club 

    """
    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request
        # SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
        if request.method in permissions.SAFE_METHODS:
            return True
        
        try:
            is_manager = Manager.objects.filter(club=obj.pk, user=request.user).exists()
        except TypeError:
            is_manager = Manager.objects.filter(club=obj.club.pk, user=request.user).exists()

        # obj : object of Recruit, Notice
        #obj_other = Manager.objects.filter(club=obj.club, user=request.user})

        return is_manager #or obj_other.exists()


class IsManager(permissions.BasePermission):
    pass