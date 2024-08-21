from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Разрешены только безопасные методы (GET, HEAD или OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешены изменения только владельцем объекта
        return obj.user == request.user