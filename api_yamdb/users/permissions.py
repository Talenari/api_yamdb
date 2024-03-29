from rest_framework import permissions


class CreatorOnlyPermission(permissions.BasePermission):
    """Пермишн для содателя объекта, модератора, администратора."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (obj.author == request.user
                 or request.user.is_moderator
                 or request.user.is_admin
                 or request.user.is_superuser)
        )


class AdminPermission(permissions.BasePermission):
    """Пермишн для администратора."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_admin
                or request.user.is_superuser)


class IsAdminOrReadPermission(permissions.BasePermission):
    """Админ может вносить изменения."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )
