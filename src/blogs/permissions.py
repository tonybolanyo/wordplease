from django.utils import timezone
from rest_framework.permissions import BasePermission


class IsOwnerAdminOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True   # obj.pub_date <= timezone.now()
        return obj.author == request.user or request.user.is_superuser
