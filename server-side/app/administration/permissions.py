from rest_framework import permissions

class AdministratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.role == 1)
        return request.method == 'GET' or admin_permission

class AdministratorOrProfessorStudentReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 1 and request.user:
            return True
        elif request.user.role == 2 or request.user.role == 3 and request.user:
            return request.method == 'GET'

class ProfessorOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 2 and request.user:
            return True
        else:
            return request.method == None