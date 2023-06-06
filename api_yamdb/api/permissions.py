from rest_framework import permissions


class AdminPermissions(permissions.BasePermission):
    """Автор получает возможность вносить изменения."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.user == request.user
        )
