from rest_framework import permissions

class AdministratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.role == 1)
        return request.method == None or admin_permission

class AdministratorOrStudentReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.role == 1)
        return request.method == 'GET' or admin_permission
