from rest_framework.permissions import BasePermission


class OperatorPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            user = request.user
            if user.user_type == 'OPERATOR':
                return True
            return False
        return True
