from rest_framework import permissions

class AdministratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.role == 1)
        return request.method == 'POST' or admin_permission