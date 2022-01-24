from rest_framework import permissions

class AdministratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.role == 1)
        return request.method == 'GET' or admin_permission

class ProfessorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        professor_permission = bool(request.user and request.user.role == 2)
        return request.method == 'None' or professor_permission