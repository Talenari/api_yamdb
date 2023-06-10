from rest_framework import permissions

from users.models import User

class CreatorOnlyPermission(permissions.BasePermission):
    """Пермишн для содателя объекта, модератора, администратора."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
                or request.user.is_superuser)


class AdminPermission(permissions.BasePermission):
    """Пермишн для администратора."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == 'admin'
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'admin'
                or request.user.is_superuser)


class IsAdminOrReadPermission(permissions.BasePermission):
    """Админ вносить изменения."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == 'admin'
        )
