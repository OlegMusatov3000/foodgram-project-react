from django.urls import resolve
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        match = resolve(request.path_info)
        if match.url_name == 'user-me' and request.user.is_anonymous:
            return False
        return (
            request.user.is_staff
            or request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, _, obj):
        if request.method in ['PATCH', 'DELETE']:
            return (
                request.user.is_staff
                or obj.author == request.user
            )
        return True
