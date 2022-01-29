from rest_framework import permissions

class AdministratorOrProfessorReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 1 and request.user:
            return True
        elif request.user.role == 2 and request.user:
            return request.method == 'GET'
        elif request.user.role == 3 and request.user:
            return request.method == None

class AdministratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.role == 1)
        return request.method == 'GET' or admin_permission