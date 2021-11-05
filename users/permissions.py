from rest_framework.permissions import BasePermission


class IsAdminOrIsMe(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user == obj


class IsAnonymousOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return not request.user.is_authenticated or request.user.is_staff
