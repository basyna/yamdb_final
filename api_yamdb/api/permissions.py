from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return (
                request.method == 'GET'
                or request.user.role == 'admin'
            )
        else:
            return request.method == 'GET'


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user or request.method == 'GET'
        )


class IsOwnerOrAdminReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            return (
                obj.author == request.user
                or request.user.role in ['admin', 'moderator']
            )
        else:
            return request.method == 'GET'


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return (
                request.user.role == 'admin' or request.user.is_superuser
            )
        return False
