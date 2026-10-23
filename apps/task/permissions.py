from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение на уровне объекта:
    - Безопасные методы (GET, HEAD, OPTIONS) доступны всем пользователям.
    - Изменение (PUT, PATCH) и удаление (DELETE) разрешены только владельцу объекта (obj.user) или администраторам (is_staff).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(
            request.user and request.user.is_authenticated and (
                obj.user == request.user or request.user.is_staff
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение на уровне запроса:
    - Безопасные методы (GET) доступны всем.
    - Небезопасные методы (POST, PUT, DELETE) доступны только персоналу (is_staff).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
